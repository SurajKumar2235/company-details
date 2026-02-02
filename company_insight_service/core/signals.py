import requests
import json
import logging
from sqlalchemy import event
from sqlalchemy.orm import Session
from company_insight_service.database.models import Company, ProductSentiment, StockAnalysis, FinancialReport
from company_insight_service.config.settings import settings
from telegram import Bot
from telegram.error import TelegramError, InvalidToken
import asyncio
import threading
from typing import Optional

logger = logging.getLogger(__name__)

# Global flag to track if credentials are valid
_credentials_validated = False
_credentials_valid = False


async def validate_telegram_credentials() -> bool:
    """
    Validates Telegram bot token and chat ID.
    Returns True if valid, False otherwise.
    """
    global _credentials_validated, _credentials_valid
    
    if _credentials_validated:
        return _credentials_valid
    
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # Check if credentials exist
    if not token or not chat_id:
        logger.error("Telegram credentials missing. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in settings.")
        _credentials_validated = True
        _credentials_valid = False
        return False
    
    # Validate token format (should be like: 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ)
    if not token or ':' not in token:
        logger.error("Invalid TELEGRAM_BOT_TOKEN format. Token should be in format: '123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ'")
        _credentials_validated = True
        _credentials_valid = False
        return False
    
    try:
        bot = Bot(token=token)
        
        # Test 1: Validate bot token
        bot_info = await bot.get_me()
        logger.info(f"✅ Bot token valid. Bot username: @{bot_info.username}")
        
        # Test 2: Check if bot can access the chat
        try:
            chat = await bot.get_chat(chat_id=chat_id)
            logger.info(f"✅ Chat ID valid. Chat title: {chat.title if chat.title else 'Private chat'}")
        except Unauthorized:
            logger.error(f"❌ Bot is not a member of chat {chat_id} or doesn't have permission to access it.")
            logger.error("Solution: Add the bot to your channel/group and make sure it has posting permissions.")
            _credentials_validated = True
            _credentials_valid = False
            return False
        except TelegramError as e:
            logger.error(f"❌ Invalid chat ID {chat_id}: {e}")
            logger.error("Solution: Make sure TELEGRAM_CHAT_ID is correct. For channels, use format: @channelname or -100xxxxxxxxxx")
            _credentials_validated = True
            _credentials_valid = False
            return False
        
        # Test 3: Try sending a test message
        test_message = "🤖 *Telegram Notifications Activated*\n\nYour bot is successfully connected and ready to send database notifications!"
        await bot.send_message(chat_id=chat_id, text=test_message, parse_mode="Markdown")
        logger.info("✅ Test message sent successfully!")
        
        _credentials_validated = True
        _credentials_valid = True
        return True
        
    except InvalidToken:
        logger.error("❌ Invalid TELEGRAM_BOT_TOKEN. Please check your bot token from @BotFather")
        _credentials_validated = True
        _credentials_valid = False
        return False
    except Exception as e:
        logger.error(f"❌ Error validating Telegram credentials: {e}", exc_info=True)
        _credentials_validated = True
        _credentials_valid = False
        return False


def send_telegram_message(text: str):
    """
    Sends a message to a Telegram channel/chat using the Bot API asynchronously.
    This function is non-blocking and runs in a separate thread.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    if not token or not chat_id:
        logger.warning("Telegram settings not configured. Skipping notification.")
        return
    
    # Check if credentials were validated and failed
    if _credentials_validated and not _credentials_valid:
        logger.debug("Skipping Telegram notification - credentials invalid")
        return
    
    async def _send():
        try:
            # Validate credentials on first use
            if not _credentials_validated:
                is_valid = await validate_telegram_credentials()
                if not is_valid:
                    logger.error("Telegram credentials validation failed. Notification skipped.")
                    return
            
            bot = Bot(token=token)
            await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
            logger.info(f"✉️ Telegram notification sent: {text[:50]}...")
            
        except Unauthorized:
            logger.error("Bot doesn't have permission to send messages. Check if bot is still in the chat/channel.")
        except TelegramError as e:
            logger.error(f"Telegram API error: {e}")
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}", exc_info=True)
    
    def run_async():
        """
        Runs the async function in a new event loop within a separate thread.
        """
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(_send())
            finally:
                loop.close()
        except Exception as e:
            logger.error(f"Error in async loop: {e}", exc_info=True)
    
    # Start thread as daemon so it doesn't block application shutdown
    thread = threading.Thread(target=run_async, daemon=True)
    thread.start()


def format_model_notification(target, operation: str) -> str:
    """
    Formatted message for database operations.
    """
    table_name = target.__tablename__
    details = ""
    
    try:
        if isinstance(target, Company):
            details = f"*Company:* {target.name}"
        elif isinstance(target, ProductSentiment):
            details = f"*Product:* {target.product_name}\n*Sentiment:* {target.sentiment_label} ({target.sentiment_score})"
        elif isinstance(target, StockAnalysis):
            details = f"*Ticker:* {target.ticker}\n*Trend:* {target.analysis_text}"
        elif isinstance(target, FinancialReport):
            details = f"*Period:* {target.period}"
        else:
            details = f"*ID:* {getattr(target, 'id', 'N/A')}"
    except AttributeError as e:
        logger.warning(f"Error accessing attributes for notification: {e}")
        details = "*Details unavailable*"
    
    return (
        f"🚨 *Database Signal*\n\n"
        f"📦 *Table:* `{table_name}`\n"
        f"⚙️ *Operation:* {operation}\n"
        f"📝 *Details:*\n{details}"
    )


def after_insert_listener(mapper, connection, target):
    """
    SQLAlchemy event listener for INSERT operations.
    Triggered after insert but before commit.
    """
    try:
        logger.debug(f"📥 INSERT detected: {target.__tablename__}")
        message = format_model_notification(target, "INSERT")
        send_telegram_message(message)
    except Exception as e:
        logger.error(f"Error in after_insert_listener: {e}", exc_info=True)


def after_update_listener(mapper, connection, target):
    """
    SQLAlchemy event listener for UPDATE operations.
    Triggered after update but before commit.
    """
    try:
        logger.debug(f"📝 UPDATE detected: {target.__tablename__}")
        message = format_model_notification(target, "UPDATE")
        send_telegram_message(message)
    except Exception as e:
        logger.error(f"Error in after_update_listener: {e}", exc_info=True)


def register_signals():
    """
    Registers SQLAlchemy event listeners for database operations.
    Call this function once during application startup.
    """
    logger.info("🔧 Registering database signals...")
    
    models_to_watch = [Company, ProductSentiment, StockAnalysis, FinancialReport]
    
    for model in models_to_watch:
        try:
            event.listen(model, 'after_insert', after_insert_listener)
            event.listen(model, 'after_update', after_update_listener)
            logger.info(f"✅ Signals registered for {model.__tablename__}")
        except Exception as e:
            logger.error(f"Failed to register signals for {model.__name__}: {e}")
    
    logger.info("🎯 Database signal registration complete")


async def test_telegram_setup():
    """
    Standalone function to test Telegram setup.
    Call this during application startup to verify configuration.
    """
    logger.info("🧪 Testing Telegram setup...")
    is_valid = await validate_telegram_credentials()
    
    if is_valid:
        logger.info("✅ Telegram is configured correctly and ready to use!")
    else:
        logger.warning("⚠️ Telegram notifications will be disabled due to configuration issues.")
    
    return is_valid


# Auto-register on import
register_signals()


# Optional: Test credentials on startup
if __name__ == "__main__":
    # Run this to test your setup
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_telegram_setup())