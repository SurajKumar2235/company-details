from telegram import Bot
import asyncio
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
import os
async def send_message():
    # Your bot token from BotFather
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # The chat ID of the person (can be a number or @username)
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if bot_token is None or chat_id is None:
        print("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in .env file")
        return
    # Create bot instance
    bot = Bot(token=bot_token)
    
    # Send the message
    await bot.send_message(
        chat_id=chat_id,
        text="Hello! This is a message from my bot."
    )
    
    print("Message sent successfully!")

# Run the async function
logging.info(asyncio.run(send_message()))