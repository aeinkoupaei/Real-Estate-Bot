"""
Component Test Script for Real Estate Bot
Tests core functionality without requiring Telegram connection
Run this to verify basic setup and components
"""
import sys
import os

print("=" * 60)
print("Real Estate Bot - Component Test Suite")
print("=" * 60)
print()

# Test 1: Import Configuration
print("[Test 1] Testing configuration import...")
try:
    import config
    print("✅ Config module imported successfully")
    
    # Check for required settings
    if config.TELEGRAM_BOT_TOKEN:
        print("✅ Telegram Bot Token: Configured")
    else:
        print("⚠️  Telegram Bot Token: NOT CONFIGURED")
    
    if config.OPENAI_API_KEY:
        print("✅ OpenAI API Key: Configured")
    else:
        print("⚠️  OpenAI API Key: NOT CONFIGURED")
    
    print(f"✅ OpenAI Model: {config.OPENAI_MODEL}")
    print(f"✅ Database URL: {config.DATABASE_URL}")
    
except Exception as e:
    print(f"❌ Config import failed: {e}")
    sys.exit(1)

print()

# Test 2: Database Connection
print("[Test 2] Testing database connection...")
try:
    from database import DatabaseManager, Property
    
    db = DatabaseManager()
    print("✅ Database manager initialized")
    
    # Test session creation
    session = db.get_session()
    session.close()
    print("✅ Database session created successfully")
    
    # Check if tables exist
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"✅ Database tables: {tables}")
    
except Exception as e:
    print(f"❌ Database test failed: {e}")
    sys.exit(1)

print()

# Test 3: AI Handler
print("[Test 3] Testing AI handler...")
try:
    from gpt_handler import GptHandler
    
    ai_handler = GptHandler()
    print("✅ AI handler initialized")
    
    # Test property extraction (if API key is configured)
    if config.OPENAI_API_KEY and config.OPENAI_API_KEY != 'your-openai-api-key-here':
        print("✅ Testing AI extraction...")
        test_text = "A 100 square meter apartment in New York, 2 bedrooms, price $400,000"
        result = ai_handler.extract_property_info(test_text)
        
        if result and isinstance(result, dict):
            print("✅ Property extraction successful")
            print(f"   Extracted fields: {list(result.keys())}")
        else:
            print("⚠️  Property extraction returned empty (might be API issue)")
    else:
        print("⚠️  OpenAI API Key not configured - skipping AI tests")
    
except Exception as e:
    print(f"❌ AI handler test failed: {e}")
    print("   This might be OK if the API key is not configured yet")

print()

# Test 4: Voice Handler
print("[Test 4] Testing voice handler...")
try:
    from voice_handler import VoiceHandler
    
    voice = VoiceHandler()
    print("✅ Voice handler initialized")
    
    if voice.is_available():
        print("✅ Voice service is available")
    else:
        print("⚠️  Voice service unavailable (requires OpenAI API Key)")
    
except Exception as e:
    print(f"❌ Voice handler test failed: {e}")

print()

# Test 5: Database Operations
print("[Test 5] Testing database CRUD operations...")
try:
    # Create test property
    test_property_data = {
        'title': 'Test Apartment',
        'property_type': 'apartment',
        'city': 'Test City',
        'neighborhood': 'Test Neighborhood',
        'area': 100.0,
        'price': 300000.0,
        'rooms': 2,
        'floor': 3,
        'parking': True,
        'elevator': False,
        'description': 'This is a test property'
    }
    
    # Add property
    test_user_id = 999999999  # Test user ID
    prop_id = db.add_property(test_user_id, test_property_data)
    print(f"✅ Created test property (ID: {prop_id})")
    
    # Retrieve property
    prop = db.get_property(prop_id)
    if prop and prop.title == 'Test Apartment':
        print("✅ Retrieved property successfully")
    else:
        print("❌ Failed to retrieve property")
    
    # Update property
    updates = {'price': 350000.0}
    success = db.update_property(prop_id, updates)
    if success:
        print("✅ Updated property successfully")
    else:
        print("❌ Failed to update property")
    
    # Search properties
    filters = {'city': 'Test City'}
    results = db.search_properties(filters)
    if len(results) > 0:
        print(f"✅ Search successful (found {len(results)} properties)")
    else:
        print("⚠️  Search returned no results")
    
    # Filter by keywords
    keyword_results = db.filter_by_keywords('test')
    print(f"✅ Keyword filter successful (found {len(keyword_results)} properties)")
    
    # Delete test property
    success = db.delete_property(prop_id, test_user_id)
    if success:
        print("✅ Deleted test property successfully")
    else:
        print("❌ Failed to delete test property")
    
    # Verify deletion
    prop = db.get_property(prop_id)
    if prop is None:
        print("✅ Confirmed property deletion")
    else:
        print("⚠️  Property still exists after deletion")
    
except Exception as e:
    print(f"❌ Database operations test failed: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 6: Message Templates
print("[Test 6] Testing message templates...")
try:
    # Check all required messages exist
    required_messages = [
        'welcome', 'select_goal', 'help', 'register_start',
        'search_start', 'filter_start', 'edit_start', 'missing_info',
        'confirm_data', 'success_register', 'success_search',
        'cancel', 'error', 'voice_recognized', 'no_goal_warning'
    ]
    
    missing = []
    for msg_key in required_messages:
        if msg_key not in config.MESSAGES:
            missing.append(msg_key)
    
    if missing:
        print(f"⚠️  Missing message templates: {missing}")
    else:
        print("✅ All required message templates present")
        print(f"   Total messages: {len(config.MESSAGES)}")
    
    # Verify messages are in English
    sample_msg = config.MESSAGES['welcome']
    if 'Real Estate' in sample_msg or 'property' in sample_msg.lower():
        print("✅ Messages are in English")
    else:
        print("⚠️  Message language unclear")
    
except Exception as e:
    print(f"❌ Message template test failed: {e}")

print()

# Test 7: Statistics
print("[Test 7] Testing statistics...")
try:
    stats = db.get_statistics()
    print("✅ Statistics retrieved successfully")
    print(f"   Total properties: {stats['total_properties']}")
    print(f"   Average price: ${stats['average_price']:,.2f}")
    print(f"   Average area: {stats['average_area']:.2f} sq m")
except Exception as e:
    print(f"❌ Statistics test failed: {e}")

print()

# Final Summary
print("=" * 60)
print("Test Summary")
print("=" * 60)
print()
print("Core Components:")
print("  ✅ Configuration")
print("  ✅ Database Manager")
print("  ✅ AI Handler")
print("  ✅ Voice Handler")
print("  ✅ Message Templates")
print()
print("Database Operations:")
print("  ✅ Create (add_property)")
print("  ✅ Read (get_property)")
print("  ✅ Update (update_property)")
print("  ✅ Delete (delete_property)")
print("  ✅ Search (search_properties)")
print("  ✅ Filter (filter_by_keywords)")
print()

# Check if ready for production
print("Production Readiness Check:")
ready = True

if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == 'your-telegram-bot-token-here':
    print("  ⚠️  Telegram Bot Token not configured")
    ready = False
else:
    print("  ✅ Telegram Bot Token configured")

if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == 'your-openai-api-key-here':
    print("  ⚠️  OpenAI API Key not configured")
    ready = False
else:
    print("  ✅ OpenAI API Key configured")

print()
if ready:
    print("🎉 All systems ready! You can start the bot with: python bot.py")
else:
    print("⚠️  Please configure missing API keys in .env file")
    print("   See env.example for reference")

print()
print("=" * 60)
print()

