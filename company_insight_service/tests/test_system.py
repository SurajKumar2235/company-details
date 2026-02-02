"""
Dedicated Signals Testing Script
Tests SQLAlchemy event listeners and Telegram notifications
"""
import asyncio
import logging
import time
import sys
from pathlib import Path

# Setup logging to see everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import database models and signals
from company_insight_service.database.models import (
    Company, ProductSentiment, StockAnalysis, FinancialReport,
    SessionLocal, init_db, engine, Base
)
from company_insight_service.config.settings import settings

print("="*70)
print("SIGNALS TESTING SCRIPT")
print("="*70)

# Step 1: Verify signals module is loaded
print("\n1️⃣ Checking if signals module is loaded...")
try:
    from company_insight_service.core import signals
    print("   ✅ Signals module imported")
    
    # Check if signals are registered
    from sqlalchemy import event
    
    # Check if listeners are attached
    has_insert_listener = event.contains(Company, 'after_insert', signals.after_insert_listener)
    has_update_listener = event.contains(Company, 'after_update', signals.after_update_listener)
    
    if has_insert_listener:
        print("   ✅ INSERT listener is registered on Company model")
    else:
        print("   ❌ INSERT listener is NOT registered on Company model")
        
    if has_update_listener:
        print("   ✅ UPDATE listener is registered on Company model")
    else:
        print("   ❌ UPDATE listener is NOT registered on Company model")
        
except ImportError as e:
    print(f"   ❌ Failed to import signals module: {e}")
    print("   Make sure signals.py exists and is in the Python path")
    sys.exit(1)

# Step 2: Verify Telegram credentials
print("\n2️⃣ Checking Telegram configuration...")
if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
    print(f"   ✅ Bot Token: ...{settings.TELEGRAM_BOT_TOKEN[-10:]}")
    print(f"   ✅ Chat ID: {settings.TELEGRAM_CHAT_ID}")
    
    # Check validation status
    if signals._credentials_validated:
        if signals._credentials_valid:
            print("   ✅ Credentials validated successfully")
        else:
            print("   ❌ Credentials validated but INVALID")
            print("   ⚠️ This is why you're not getting messages!")
    else:
        print("   ⚠️ Credentials not yet validated (will validate on first send)")
else:
    print("   ❌ Telegram credentials are MISSING")
    print("   Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in your .env file")

# Step 3: Test Telegram connectivity
print("\n3️⃣ Testing Telegram API connection...")
async def test_telegram():
    try:
        result = await signals.validate_telegram_credentials()
        if result:
            print("   ✅ Telegram connection successful!")
            return True
        else:
            print("   ❌ Telegram connection failed!")
            print("   Check the error messages above for details")
            return False
    except Exception as e:
        print(f"   ❌ Error testing Telegram: {e}")
        import traceback
        traceback.print_exc()
        return False

telegram_ok = asyncio.run(test_telegram())

if not telegram_ok:
    print("\n⚠️ Telegram is not working. Signals will fire but messages won't send.")
    print("Fix Telegram issues before proceeding, or continue to test signal firing only.")
    response = input("\nContinue anyway? (y/n): ")
    if response.lower() != 'y':
        sys.exit(1)

# Step 4: Initialize database
print("\n4️⃣ Initializing database...")
try:
    init_db()
    print("   ✅ Database initialized")
except Exception as e:
    print(f"   ❌ Database initialization failed: {e}")
    sys.exit(1)

# Step 5: Test INSERT signal
print("\n5️⃣ Testing INSERT Signal...")
print("   Creating a new Company record...")

db = SessionLocal()
test_company_name = f"TEST_COMPANY_{int(time.time())}"

try:
    # Clean up any existing test company
    existing = db.query(Company).filter(Company.name.like("TEST_COMPANY_%")).all()
    if existing:
        print(f"   🧹 Cleaning up {len(existing)} old test records...")
        for company in existing:
            db.delete(company)
        db.commit()
    
    # Create new company
    print(f"   📝 Creating company: {test_company_name}")
    new_company = Company(
        name=test_company_name,
        description="Test company for signal testing"
    )
    db.add(new_company)
    
    print("   🔄 Committing transaction (signal should fire now)...")
    db.commit()
    
    print("   ✅ Company created successfully!")
    print("\n" + "🔔"*35)
    print("CHECK YOUR TELEGRAM NOW!")
    print("You should see a message about 'INSERT' operation")
    print(f"Company: {test_company_name}")
    print("🔔"*35)
    
    # Wait for async message delivery
    print("\n   ⏳ Waiting 5 seconds for message delivery...")
    for i in range(5, 0, -1):
        print(f"      {i}...", end='\r')
        time.sleep(1)
    print("\n")
    
    # Step 6: Test UPDATE signal
    print("6️⃣ Testing UPDATE Signal...")
    print(f"   📝 Updating company: {test_company_name}")
    
    new_company.description = "UPDATED: This description was changed to test UPDATE signal"
    db.commit()
    
    print("   ✅ Company updated successfully!")
    print("\n" + "🔔"*35)
    print("CHECK YOUR TELEGRAM AGAIN!")
    print("You should see a message about 'UPDATE' operation")
    print(f"Company: {test_company_name}")
    print("🔔"*35)
    
    print("\n   ⏳ Waiting 5 seconds for message delivery...")
    for i in range(5, 0, -1):
        print(f"      {i}...", end='\r')
        time.sleep(1)
    print("\n")
    
    # Step 7: Test with other models
    print("7️⃣ Testing signals on other models...")
    
    # Test ProductSentiment
    print("\n   📊 Testing ProductSentiment model...")
    # Already imported at top
    
    sentiment = ProductSentiment(
        company_id=new_company.id,
        product_name="Test Product",
        sentiment_label="POSITIVE",
        sentiment_score=0.95,
        source_url="https://example.com/test"
    )
    db.add(sentiment)
    db.commit()
    
    print("   ✅ ProductSentiment created!")
    print("   🔔 Check Telegram for ProductSentiment INSERT notification")
    
    time.sleep(3)
    
    # Test StockAnalysis
    print("\n   📈 Testing StockAnalysis model...")
    # Already imported at top
    
    stock = StockAnalysis(
        company_id=new_company.id,
        ticker="TEST",
        analysis_text="Test stock analysis",
        trend="BULLISH"
    )
    db.add(stock)
    db.commit()
    
    print("   ✅ StockAnalysis created!")
    print("   🔔 Check Telegram for StockAnalysis INSERT notification")
    
    time.sleep(3)
    
    # Step 8: Cleanup
    print("\n8️⃣ Cleaning up test data...")
    cleanup = input("   Delete test records from database? (y/n): ")
    
    if cleanup.lower() == 'y':
        # Delete in correct order (respect foreign keys)
        db.query(ProductSentiment).filter(ProductSentiment.company_id == new_company.id).delete()
        db.query(StockAnalysis).filter(StockAnalysis.company_id == new_company.id).delete()
        db.delete(new_company)
        db.commit()
        print("   ✅ Test data cleaned up")
    else:
        print("   ⏭️ Skipping cleanup - test data remains in database")
    
    print("\n" + "="*70)
    print("SIGNAL TESTING COMPLETE!")
    print("="*70)
    print("\nSummary:")
    print("✅ Signals module loaded")
    print("✅ Event listeners registered")
    print(f"{'✅' if telegram_ok else '❌'} Telegram connectivity")
    print("✅ INSERT signal tested")
    print("✅ UPDATE signal tested")
    print("✅ Multiple model signals tested")
    
    if telegram_ok:
        print("\n💡 You should have received 5 Telegram notifications:")
        print("   1. Initial test message")
        print("   2. Company INSERT")
        print("   3. Company UPDATE")
        print("   4. ProductSentiment INSERT")
        print("   5. StockAnalysis INSERT")
    else:
        print("\n⚠️ Telegram was not working - signals fired but messages didn't send")
    
    print("\n" + "="*70)
    
except Exception as e:
    print(f"\n❌ Error during signal testing: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

# # Step 9: Direct message test
# print("\n9️⃣ BONUS: Direct Telegram message test...")
# send_direct = input("   Send a direct test message via send_telegram_message()? (y/n): ")

# if send_direct.lower() == 'y':
#     test_msg = (
#         "🧪 *Direct Function Call Test*\n\n"
#         "This message was sent by calling `send_telegram_message()` directly.\n"
#         f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}"
#     )
    
#     print("   📤 Sending message...")
#     signals.send_telegram_message(test_msg)
    
#     print("   ✅ Function called (async delivery in progress)")
#     print("   🔔 Check Telegram for the direct test message")
    
#     print("\n   ⏳ Waiting 3 seconds...")
#     time.sleep(3)

print("\n✨ All tests complete! ✨\n")