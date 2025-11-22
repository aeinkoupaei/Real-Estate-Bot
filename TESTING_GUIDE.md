# Testing Guide - Real Estate Chatbot

This guide will help you test all features of the real estate management chatbot to ensure everything works correctly.

---

## Pre-Testing Checklist

Before starting tests, ensure:

- `.env` file is configured with:
  - `TELEGRAM_BOT_TOKEN` (from BotFather)
  - `OPENAI_API_KEY` (from OpenAI Platform)
- Virtual environment is activated: `source realassist/bin/activate`
- All dependencies installed: `pip install -r requirements.txt`
- Bot is running: `python bot.py`

---

## Test Suite

### Test 1: Bot Startup and Welcome

**Objective**: Verify bot starts correctly and shows goal selection

**Steps**:
1. Start conversation with bot
2. Send `/start` command

**Expected Result**:
```
Welcome to the Real Estate Management Chatbot!

I'm your intelligent assistant for managing property information. 

**Please select your goal first:**
- Register a property
- Search for a property
- Filter properties by keyword
- Edit a property
- View my properties

You can select from the menu below or type your goal directly.

 **Both text and voice input are supported!**
```

**Pass Criteria**: 
- Welcome message appears
- Goal selection buttons are shown
- All 6 buttons present: Register, Search, Filter, Edit, List, Help

---

### Test 2: Goal-First Enforcement

**Objective**: Verify bot requires goal selection before processing

**Steps**:
1. Send `/start`
2. **Without** clicking any goal button, type: "I have an apartment"

**Expected Result**:
```
WARNING:  Please specify your goal first. What would you like to do?

Select an option from the menu below:
```
[Goal selection menu appears again]

**Pass Criteria**:
- Bot does NOT process the property information
- Bot shows warning message
- Goal selection menu appears

---

### Test 3: Register Property - Text Input (Complete Info)

**Objective**: Test full registration flow with all information provided at once

**Steps**:
1. Click " Register Property" button
2. Type: "Modern Apartment in New York, Manhattan, 120 square meters, 2 bedrooms, 3rd floor, built in 2015, has parking and elevator, price $500,000"

**Expected Result**:
```
Processing...  Processing your information...

WARNING:  Some information is missing:
- Property title

I've already saved:
 Type: apartment
City City: New York
Location Neighborhood: Manhattan
Area Area: 120.00
Price Price: 500,000.00
Bedrooms Bedrooms: 2
Floor Floor: 3
Year Built Year Built: 2015
Parking Parking: Yes
Elevator Elevator: Yes

You can type or send a voice message with the missing information.
```

3. Type: "Luxury Manhattan Apartment"

**Expected Result**:
```
 Here's the information I have collected:

Title: Luxury Manhattan Apartment
Type: apartment
City City: New York
Location Neighborhood: Manhattan
Area Area: 120.00
Price Price: 500,000.00
Bedrooms Bedrooms: 2
Floor Floor: 3
Year Built Year Built: 2015
Parking Parking: Yes
Elevator Elevator: Yes

Would you like to:
- **Confirm and submit** - Type "confirm" or "yes"
- **Add/Edit information** - Just tell me what to change
- **Cancel** - Type "cancel" or /cancel

What would you like to do?
```

4. Type: "confirm"

**Expected Result**:
```
 Your property has been successfully registered!

[Shows full property details with ID]

What would you like to do next?
[Goal selection menu]
```

**Pass Criteria**:
- All information extracted correctly
- Missing title detected
- Confirmation summary shown
- Property saved to database
- Returns to goal selection

---

### Test 4: Register Property - Incremental Input (Stateful Memory)

**Objective**: Test that bot remembers previous inputs

**Steps**:
1. Click " Register Property"
2. Type: "I have an apartment"
3. Wait for response
4. Type: "In Los Angeles"
5. Wait for response
6. Type: "100 square meters"
7. Wait for response
8. Type: "$400,000"
9. Wait for response
10. Type: "Downtown LA Apartment"

**Expected Result**:
- After each message, bot acknowledges and processes
- Bot never asks to re-enter previous information
- Each new message **adds to** existing data, not replaces
- Final confirmation shows ALL accumulated information

**Pass Criteria**:
- Bot accumulates all information across multiple messages
- No data loss between messages
- Final summary includes all provided information

---

### Test 5: Register Property - Voice Input

**Objective**: Test voice message recognition and processing

**Steps**:
1. Click " Register Property"
2. Record and send voice message: "I want to register a two bedroom house in San Francisco, fifteen hundred square feet, has a garage, price seven hundred thousand dollars"

**Expected Result**:
```
Voice Converting voice to text...

Voice Voice recognized:
"I want to register a two bedroom house in San Francisco, fifteen hundred square feet, has a garage, price seven hundred thousand dollars"

Processing your request...

WARNING:  Some information is missing:
- Property title

I've already saved:
 Type: house
City City: San Francisco
Area Area: 1500.00
Price Price: 700,000.00
Bedrooms Bedrooms: 2
Parking Parking: Yes
```

3. Send voice message: "San Francisco Family Home"

**Expected Result**:
- Voice recognized correctly
- Shows confirmation summary
- Can type "confirm" to save

**Pass Criteria**:
- Voice converted to text
- Recognized text shown to user
- Information extracted correctly from voice
- Works same as text input

---

### Test 6: Search Properties

**Objective**: Test property search functionality

**Setup**: Ensure at least 3-5 properties are registered first

**Steps**:
1. Click "Search  Search Properties"
2. Type: "2 bedroom apartment under $600,000"

**Expected Result**:
```
Search  Searching for properties...

 Found X properties!

[Shows matching properties with details]
```

**Pass Criteria**:
- Search filters extracted from text
- Only matching properties shown
- Each property shows: title, location, price, specs
- Action buttons available (View Details)

---

### Test 7: Search with Voice

**Objective**: Test voice search

**Steps**:
1. Click "Search  Search Properties"
2. Send voice message: "Find me a house in Los Angeles with at least three bedrooms"

**Expected Result**:
- Voice recognized
- Search executed
- Results shown

**Pass Criteria**:
- Voice search works like text search
- Correct filters applied

---

### Test 8: Filter by Keyword

**Objective**: Test keyword filtering

**Steps**:
1. Click "Filter  Filter by Keyword"
2. Type: "luxury"

**Expected Result**:
- Shows properties containing "luxury" in any text field
- Could match title, description, address, etc.

**Pass Criteria**:
- Keyword search works
- Shows relevant results

---

### Test 9: View My Properties

**Objective**: Test viewing user's properties

**Steps**:
1. Click " My Properties"

**Expected Result**:
```
 You have X properties:

[Lists all your properties with details]
```

**Pass Criteria**:
- Shows only current user's properties
- Each property has View/Delete buttons
- Correct count shown

---

### Test 10: Edit Property

**Objective**: Test property editing with text

**Steps**:
1. Click "Edit Edit Property"
2. Select a property by clicking "Edit Edit This Property"
3. Type: "Change price to $550,000"

**Expected Result**:
```
Processing...  Processing updates...

 Property updated successfully!

[Shows updated property with new price]
```

**Pass Criteria**:
- Property selected correctly
- Update applied
- Only specified field changed
- Other fields remain unchanged

---

### Test 11: Edit Property with Voice

**Objective**: Test property editing with voice

**Steps**:
1. Click "Edit Edit Property"
2. Select a property
3. Send voice message: "Add that it has a swimming pool and change the price to six hundred thousand"

**Expected Result**:
- Voice recognized
- Updates applied
- Shows updated property

**Pass Criteria**:
- Voice editing works
- Multiple changes in one voice message work

---

### Test 12: Cancel Operation

**Objective**: Test cancellation at any point

**Steps**:
1. Click " Register Property"
2. Type: "I have an apartment in Boston"
3. Type: `/cancel`

**Expected Result**:
```
ERROR:  Operation cancelled.

What would you like to do next?
[Goal selection menu]
```

**Pass Criteria**:
- Operation stopped immediately
- Data cleared
- Returns to goal selection
- No error messages

---

### Test 13: Confirmation Flow - Edit Before Submit

**Objective**: Test editing data during confirmation

**Steps**:
1. Register a property (provide all info)
2. At confirmation stage, instead of "confirm", type: "Change price to $450,000"

**Expected Result**:
- Price updated
- New confirmation summary shown with updated price
- Other fields unchanged

**Pass Criteria**:
- Can edit during confirmation
- Changes applied correctly
- Returns to confirmation state

---

### Test 14: Confirmation Flow - Cancel at Confirmation

**Objective**: Test canceling at confirmation stage

**Steps**:
1. Register a property (provide all info)
2. At confirmation stage, type: "cancel"

**Expected Result**:
- Operation cancelled
- Property NOT saved
- Returns to goal selection

**Pass Criteria**:
- Cancel works at confirmation
- No property saved to database

---

### Test 15: Delete Property

**Objective**: Test property deletion

**Steps**:
1. Click " My Properties"
2. Click "Delete Delete" on a property
3. Confirmation dialog appears
4. Click " Yes, Delete"

**Expected Result**:
```
 Property successfully deleted.
```

**Pass Criteria**:
- Confirmation required before delete
- Property removed from database
- Can cancel deletion

---

### Test 16: Help Command

**Objective**: Test help information

**Steps**:
1. Type `/help`

**Expected Result**:
- Shows comprehensive help text
- Explains commands
- Describes how to use the bot

**Pass Criteria**:
- Help text displayed
- Information accurate and clear

---

### Test 17: Multiple Properties Registration

**Objective**: Test registering multiple properties in sequence

**Steps**:
1. Register property #1 (confirm and complete)
2. Immediately register property #2 (confirm and complete)
3. Register property #3 (confirm and complete)

**Expected Result**:
- Each property saved independently
- No data mixing between properties
- Each returns to goal selection after completion

**Pass Criteria**:
- No cross-contamination of data
- All properties saved correctly
- Session data cleared between registrations

---

### Test 18: Empty Search Results

**Objective**: Test behavior when no properties match

**Steps**:
1. Click "Search  Search Properties"
2. Type: "10 bedroom mansion price $50,000,000"

**Expected Result**:
```
No results. No properties found matching your criteria.

Try:
- Broadening your search criteria
- Removing some filters
- Searching in a different location
```

**Pass Criteria**:
- Friendly "no results" message
- Suggestions provided
- Returns to goal selection

---

### Test 19: Voice Service Unavailable

**Objective**: Test graceful handling when voice service fails

**Steps**:
1. Temporarily set invalid OPENAI_API_KEY in .env
2. Restart bot
3. Try to send a voice message

**Expected Result**:
```
ERROR:  Voice service is currently unavailable.

Please make sure:
1. OPENAI_API_KEY is configured in .env
2. You have restarted the bot
3. VPN is active if needed

You can continue using text input.
```

**Pass Criteria**:
- Error message clear and helpful
- Bot doesn't crash
- Text input still works
- User can continue without voice

**Cleanup**: Reset OPENAI_API_KEY to correct value and restart bot

---

### Test 20: Long Description Input

**Objective**: Test handling of long, detailed descriptions

**Steps**:
1. Click " Register Property"
2. Type a very long message with lots of details (150+ words)

**Expected Result**:
- Bot processes without error
- Extracts relevant information
- Ignores irrelevant parts

**Pass Criteria**:
- No crashes or timeouts
- Correct information extracted
- Handles verbose input gracefully

---

## Test Results Summary Template

Use this template to record your test results:

```
Test Date: ___________
Tester: ___________

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Bot Startup | - [ ] Pass - [ ] Fail | |
| 2 | Goal-First Enforcement | - [ ] Pass - [ ] Fail | |
| 3 | Register Complete | - [ ] Pass - [ ] Fail | |
| 4 | Register Incremental | - [ ] Pass - [ ] Fail | |
| 5 | Register Voice | - [ ] Pass - [ ] Fail | |
| 6 | Search Text | - [ ] Pass - [ ] Fail | |
| 7 | Search Voice | - [ ] Pass - [ ] Fail | |
| 8 | Filter Keyword | - [ ] Pass - [ ] Fail | |
| 9 | View Properties | - [ ] Pass - [ ] Fail | |
| 10 | Edit Text | - [ ] Pass - [ ] Fail | |
| 11 | Edit Voice | - [ ] Pass - [ ] Fail | |
| 12 | Cancel Operation | - [ ] Pass - [ ] Fail | |
| 13 | Edit at Confirmation | - [ ] Pass - [ ] Fail | |
| 14 | Cancel at Confirmation | - [ ] Pass - [ ] Fail | |
| 15 | Delete Property | - [ ] Pass - [ ] Fail | |
| 16 | Help Command | - [ ] Pass - [ ] Fail | |
| 17 | Multiple Properties | - [ ] Pass - [ ] Fail | |
| 18 | Empty Search | - [ ] Pass - [ ] Fail | |
| 19 | Voice Unavailable | - [ ] Pass - [ ] Fail | |
| 20 | Long Description | - [ ] Pass - [ ] Fail | |

Overall Result: - [ ] All Pass - [ ] Some Failures

Failures Detail:
_______________________________________________
_______________________________________________
```

---

## Quick Smoke Test (5 minutes)

If you don't have time for full testing, run this quick smoke test:

1. Start bot - verify welcome message
2. Try sending message without goal - verify warning
3. Register one property with text - verify it saves
4. Register one property with voice - verify voice works
5. Search for a property - verify results shown
6. View your properties - verify list displayed
7. Use /cancel - verify returns to menu

If all 7 pass, core functionality is working!

---

## Troubleshooting Test Failures

### Bot Not Starting
- Check TELEGRAM_BOT_TOKEN in .env
- Check OPENAI_API_KEY in .env
- Verify virtual environment activated
- Check for Python errors in terminal

### Voice Not Working
- Verify OPENAI_API_KEY is valid
- Check internet connection
- Try with VPN if in restricted region
- Test with text input to isolate issue

### Properties Not Saving
- Check database file exists (real_estate.db)
- Verify write permissions
- Check for database errors in terminal logs

### Search Returns Nothing
- Verify properties exist in database
- Check search criteria aren't too restrictive
- Try broader search terms

---

## Performance Benchmarks

Expected performance:

- Bot startup: < 5 seconds
- Text message processing: 1-3 seconds
- Voice conversion: 2-5 seconds
- Database operations: < 1 second
- Search results: 1-2 seconds

If significantly slower, check:
- Internet connection speed
- OpenAI API rate limits
- Database size (optimize if > 10,000 properties)

---

## Conclusion

After completing all tests, you should have verified:

- Goal-first approach enforced  
- Voice input works for all actions  
- Stateful memory preserves information  
- Confirmation flow allows review/edit  
- Cancel works at any point  
- All CRUD operations functional  
- Error handling graceful  
- English interface throughout  

Happy testing!

