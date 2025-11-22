# Real Estate Management Chatbot - Usage Guide

## Overview

This is a fully interactive real estate management chatbot with **goal-first approach**, **voice support**, and **stateful memory**. The bot guides users step by step and remembers all previously entered data.

## Key Features

✅ **Goal-First Design**: Must select goal before any interaction  
✅ **Voice & Text Support**: Use voice messages or text for all inputs  
✅ **Stateful Memory**: Never re-enter information - bot remembers everything  
✅ **Smart Confirmation**: Review and edit before submitting  
✅ **Cancel Anytime**: Use /cancel to restart  
✅ **English Interface**: All messages and interactions in English

---

## Getting Started

### 1. Start the Bot

Send `/start` command or press the Start button.

**Bot Response:**
```
🏠 Welcome to the Real Estate Management Chatbot!

I'm your intelligent assistant for managing property information. 🤖

**Please select your goal first:**
• Register a property
• Search for a property
• Filter properties by keyword
• Edit a property
• View my properties

You can select from the menu below or type your goal directly.

💬 **Both text and voice input are supported!**
```

---

## Available Goals

### 🏠 Register a Property

**Purpose**: Add a new property to the system

**How to use**:
1. Click "Register Property" button OR type "register" or "add property"
2. Provide property details (text or voice)
3. Bot will remember all information
4. If something is missing, bot will ask specifically for that
5. Review the summary
6. Type "confirm" or "yes" to save

**Example Text Input**:
```
A 120 square meter apartment in New York, Brooklyn, 2 bedrooms, 
3rd floor, built in 2015, has parking and elevator, price $500,000
```

**Example Voice Input**:
🎤 Speak: "I want to register a two bedroom apartment in Manhattan, 
one thousand square feet, price five hundred thousand dollars"

**Required Information**:
- Property type (apartment, house, villa, land, etc.)
- City
- Area/Size
- Price
- Title (will be auto-generated if not provided)

**Optional Information**:
- Neighborhood
- Address
- Number of bedrooms
- Floor number
- Year built
- Parking (yes/no)
- Elevator (yes/no)
- Storage room (yes/no)
- Additional description

**Step-by-Step Example**:

```
User: I have an apartment in New York
Bot: ⚠️ Some information is missing:
     • Size/Area
     • Price
     Please provide the missing details.

User: 120 square meters, $450,000
Bot: ⚠️ Some information is missing:
     • Property title
     I've already saved:
     🏢 Type: apartment
     🌆 City: New York
     📐 Area: 120
     💰 Price: 450000
     
User: Modern Downtown Apartment
Bot: ✅ Here's the information I have collected:
     🏠 Title: Modern Downtown Apartment
     🏢 Type: apartment
     🌆 City: New York
     📐 Area: 120.00
     💰 Price: 450,000.00
     
     Would you like to:
     • Confirm and submit - Type "confirm" or "yes"
     • Add/Edit information - Just tell me what to change
     • Cancel - Type "cancel"

User: confirm
Bot: ✅ Your property has been successfully registered!
```

---

### 🔍 Search for Properties

**Purpose**: Find properties based on criteria

**How to use**:
1. Click "Search Properties" OR type "search" or "find"
2. Describe what you're looking for (text or voice)
3. Bot will show matching properties

**Example Text Input**:
```
2-bedroom apartment in Manhattan, price under $600,000, with parking
```

**Example Voice Input**:
🎤 Speak: "Find me a house in Brooklyn with at least three bedrooms"

**Search Criteria**:
- Property type
- Location (city, neighborhood)
- Price range (min/max)
- Size range (min/max)
- Number of bedrooms
- Amenities (parking, elevator)

**Example**:
```
User: Search for apartments in New York
Bot: 🔍 Searching for properties...
     ✅ Found 15 properties!
     
     [Shows first 10 properties with details]
     
     📌 5 more properties found.
     Please refine your search to see more specific results.
```

---

### 🔎 Filter by Keyword

**Purpose**: Search by keywords in descriptions

**How to use**:
1. Click "Filter by Keyword" OR type "filter"
2. Enter keywords to search

**Examples**:
- "luxury penthouse"
- "garden"
- "newly renovated"
- "near subway"
- "waterfront"

---

### ✏️ Edit a Property

**Purpose**: Update information for your properties

**How to use**:
1. Click "Edit Property" OR type "edit"
2. Bot shows your properties
3. Select property to edit
4. Tell bot what to change (text or voice)

**Example**:
```
User: edit
Bot: 📋 You have 3 properties:
     Select a property to edit:
     
     [Shows your properties with "Edit This Property" buttons]

User: [Clicks "Edit This Property" for property #123]
Bot: ✏️ Editing property #123
     Tell me what you want to change.

User: Change price to $550,000 and add elevator
Bot: ✅ Property updated successfully!
```

---

### 📋 View My Properties

**Purpose**: See all your registered properties

**How to use**:
1. Click "My Properties" OR type "list" or "show my properties"
2. Bot displays all your properties

---

## Voice Input Support

### How to Use Voice

1. **Record a voice message** instead of typing
2. Bot will **convert to text** using OpenAI's transcription model
3. Bot shows you **what it heard** for confirmation
4. Bot **processes your request** automatically

### Voice Examples

**Registering a property**:
🎤 "I want to register a three bedroom house in Los Angeles, two thousand square feet, has a garage and a pool, price is eight hundred thousand dollars"

**Searching**:
🎤 "Find me a two bedroom apartment in Manhattan under five hundred thousand dollars with parking"

**Editing**:
🎤 "Change the price to six hundred thousand and add that it has a balcony"

**Confirming**:
🎤 "Yes, confirm and save it"

### Supported Languages

Primary: **English**  
The voice recognition system is optimized for English but may work with other languages.

---

## Stateful Memory (Smart Data Handling)

### How It Works

The bot **remembers everything you tell it** in the current session. You never need to repeat information.

### Example Flow

```
Session Start
-------------
User: I have an apartment
Bot: [Saves: type = apartment]

User: In New York
Bot: [Saves: type = apartment, city = New York]

User: 120 square meters
Bot: [Saves: type = apartment, city = New York, area = 120]

User: $500,000
Bot: [Saves: type = apartment, city = New York, area = 120, price = 500000]

User: 2 bedrooms, parking available
Bot: [Saves: type = apartment, city = New York, area = 120, price = 500000, 
     rooms = 2, parking = true]
     
Bot: ⚠️ Some information is missing:
     • Property title
     
User: Cozy Manhattan Apartment
Bot: ✅ All information complete! [Shows summary]
```

### Adding Information Later

```
Bot: ✅ Here's what I have:
     🏠 Title: Manhattan Apartment
     🏢 Type: apartment
     🌆 City: New York
     📐 Area: 120
     💰 Price: 500,000
     
User: Also add that it has an elevator
Bot: [Updates: adds elevator = true]
     ✅ Updated! [Shows new summary]
```

---

## Confirmation Flow

Before saving any property, the bot will:

1. **Show complete summary** of collected information
2. **Ask for confirmation**
3. **Allow edits** if needed

### Confirmation Options

**To Submit**:
- Type: `confirm`, `yes`, `ok`, `correct`, `submit`, or `save`
- Voice: 🎤 "Yes, confirm it" or "Save it"

**To Edit**:
- Type what you want to change: `change price to $600,000`
- Voice: 🎤 "Change the price to six hundred thousand"

**To Cancel**:
- Type: `cancel`, `no`, or use `/cancel` command
- Voice: 🎤 "Cancel" or "No, stop"

---

## Commands

- `/start` - Start bot and select goal
- `/help` - Show help information
- `/cancel` - Cancel current operation and return to goal selection

---

## Important Rules

### ⚠️ Goal First Rule

**You MUST select a goal before the bot will process any requests.**

**Wrong ❌**:
```
User: I have an apartment to register
Bot: ⚠️ Please specify your goal first. What would you like to do?
     [Shows goal selection menu]
```

**Correct ✅**:
```
User: [Clicks "Register Property" OR types "register"]
Bot: 📝 Register a New Property
     Please provide the property details...

User: I have an apartment in New York
Bot: ⏳ Processing your information...
```

### Cancel Anytime

Use `/cancel` at any point to:
- Stop current operation
- Clear all temporary data
- Return to goal selection menu

### Voice Availability

If voice service is unavailable, the bot will show:
```
❌ Voice service is currently unavailable.

Please make sure:
1. OPENAI_API_KEY is configured in .env
2. You have restarted the bot
3. VPN is active if needed

You can continue using text input.
```

---

## Tips for Best Experience

### 1. Be Specific
**Good**: "2-bedroom apartment in Manhattan, 1000 sq ft, $450,000"  
**Less Good**: "apartment"

### 2. Use Natural Language
You can type or speak naturally - the AI understands context!

**Examples**:
- "I'm looking for a house with a garden"
- "My budget is under half a million"
- "It should have parking"

### 3. Add Information Gradually
You don't need to provide everything at once:
```
User: Apartment in New York
[Bot acknowledges]
User: 2 bedrooms
[Bot acknowledges]
User: $500,000
[Bot acknowledges]
```

### 4. Review Before Confirming
Always check the summary before typing "confirm"

### 5. Use Voice for Long Descriptions
Instead of typing a long message, just record it!

---

## Troubleshooting

### Bot Not Responding to My Messages

**Cause**: You haven't selected a goal yet  
**Solution**: Click a goal button or type your goal (register/search/edit/list)

### Voice Not Working

**Cause**: Voice service unavailable  
**Solution**: 
1. Check .env file has GEMINI_API_KEY
2. Restart the bot
3. Enable VPN if in restricted region
4. Use text input as alternative

### Information Not Saving

**Cause**: Session data cleared or bot restarted  
**Solution**: 
- Each conversation session is independent
- Use /cancel to reset and start fresh
- Avoid restarting bot mid-conversation

### Can't Find Properties

**Cause**: Search criteria too restrictive  
**Solution**: 
- Broaden your search
- Remove some filters
- Try searching in different location

---

## Example Complete Flow

### Full Registration Flow

```
1. User: /start
2. Bot: [Shows welcome and goal selection menu]

3. User: [Clicks "Register Property"]
4. Bot: 📝 Register a New Property
      Please provide the property details...

5. User: 🎤 [Voice] "I have a beautiful two bedroom apartment 
   in Manhattan, it's one hundred twenty square meters, has parking 
   and an elevator, third floor, built in twenty fifteen, 
   price is five hundred thousand dollars"

6. Bot: 🎤 Voice recognized:
      "I have a beautiful two bedroom apartment in Manhattan, 
      it's 120 square meters, has parking and an elevator, 
      third floor, built in 2015, price is $500,000"
      
      Processing your request...

7. Bot: ⚠️ Some information is missing:
      • Property title
      
      I've already saved:
      🏢 Type: apartment
      🌆 City: Manhattan
      📐 Area: 120.00
      💰 Price: 500,000.00
      🛏 Bedrooms: 2
      🏗 Floor: 3
      📅 Year Built: 2015
      🅿️ Parking: Yes
      🛗 Elevator: Yes

8. User: Modern Manhattan Apartment

9. Bot: ✅ Here's the information I have collected:
      🏠 Title: Modern Manhattan Apartment
      🏢 Type: apartment
      🌆 City: Manhattan
      📐 Area: 120.00
      💰 Price: 500,000.00
      🛏 Bedrooms: 2
      🏗 Floor: 3
      📅 Year Built: 2015
      🅿️ Parking: Yes
      🛗 Elevator: Yes
      
      Would you like to:
      • Confirm and submit - Type "confirm" or "yes"
      • Add/Edit information - Just tell me what to change
      • Cancel - Type "cancel"

10. User: yes

11. Bot: ✅ Your property has been successfully registered!
       [Shows full property details with ID]
       
       What would you like to do next?
       [Shows goal selection menu]
```

---

## Summary

This chatbot provides a **complete, user-friendly experience** for managing real estate properties with:

- ✅ **Goal-first approach**: Always know what you're doing
- ✅ **Voice support**: Speak naturally instead of typing
- ✅ **Smart memory**: Never repeat information
- ✅ **Confirmation flow**: Review before submitting
- ✅ **Cancel anytime**: Full control over the process
- ✅ **English interface**: Clear, professional communication

Enjoy using your intelligent real estate assistant! 🏠🤖

