# Interactive Demo Guide

This guide shows you how to test and demonstrate all features of the Real Estate Chatbot.

## Quick Demo (5 minutes)

### Step 1: Start the Bot

```bash
# Activate virtual environment
source realassist/bin/activate

# Start bot
python bot.py
```

You should see:
```
✅ Bot successfully launched!
🔗 Press Ctrl+C to stop.
```

### Step 2: Open Telegram

1. Open Telegram app
2. Search for your bot (the name you gave it in BotFather)
3. Click **Start** or send `/start`

### Step 3: Test Basic Flow

**Test Goal Selection:**
```
1. Bot shows welcome message with menu
2. Try sending a message WITHOUT clicking a goal
3. Bot should show: "⚠️ Please specify your goal first"
```

**Test Property Registration:**
```
1. Click "🏠 Register Property"
2. Type: "Luxury apartment in New York, Manhattan, 1200 square feet, 
   2 bedrooms, 10th floor, built in 2020, price $650,000, has parking and elevator"
3. Bot processes and shows summary
4. Type "confirm"
5. Bot saves property successfully
```

**Test Voice Input:**
```
1. Click "🏠 Register Property" again
2. Hold microphone button in Telegram
3. Say: "Two bedroom house in Los Angeles, 1500 square feet, 
   has garage and pool, price seven hundred thousand dollars"
4. Release button
5. Bot converts voice to text
6. Bot processes and asks for missing info (if any)
```

**Test Search:**
```
1. Click "🔍 Search Properties"
2. Type: "2 bedroom apartment under $700,000"
3. Bot shows matching properties
```

**Test Edit with Filtering:**
```
1. Click "✏️ Edit Property"
2. Bot asks: "Which property would you like to edit? 
   Describe it or say 'show all properties'"
3. Type: "apartment in New York priced at $650,000"
4. Bot filters and shows matching property
5. Click "✏️ Edit This Property"
6. Type: "Change price to $700,000 and delete the description"
7. Bot updates successfully
```

---

## Complete Demo Script

### Demo 1: Complete Registration Flow

**What to show:**
- Goal selection requirement
- Natural language input
- Stateful memory
- Confirmation flow

**Script:**
```
1. /start
   → Shows welcome and goal menu

2. [Click "Register Property"]
   → Bot asks for property details

3. Type: "I have an apartment"
   → Bot extracts: type = apartment

4. Type: "In San Francisco"
   → Bot extracts: city = San Francisco
   → Bot remembers: type = apartment

5. Type: "1200 square feet, 2 bedrooms, $800,000"
   → Bot extracts: area, rooms, price
   → Bot remembers all previous info

6. Bot shows: "⚠️ Missing: Property title"
   → Shows what it has saved so far

7. Type: "Modern SF Apartment"
   → Bot shows complete summary

8. Type: "confirm"
   → Bot saves successfully
```

### Demo 2: Voice Input

**What to show:**
- Voice-to-text conversion
- Natural language processing
- Same functionality as text

**Script:**
```
1. [Click "Register Property"]

2. 🎤 [Send voice message]
   Say: "Luxury penthouse in Miami Beach, 2500 square feet, 
   3 bedrooms, 20th floor, ocean view, price one point two million dollars"

3. Bot shows: "🎤 Voice recognized: [transcribed text]"
   → Shows what it understood

4. Bot processes and shows summary
   → Same as text input

5. Type: "confirm"
   → Saves successfully
```

### Demo 3: Incomplete Data Handling

**What to show:**
- Missing field detection
- Smart prompts
- Incremental data collection

**Script:**
```
1. [Click "Register Property"]

2. Type: "House in Austin, 3 bedrooms"
   → Bot extracts: type, city, rooms
   → Bot shows: "⚠️ Missing: area, price, title"

3. Type: "2500 square feet"
   → Bot updates: area = 2500
   → Bot still shows: "⚠️ Missing: price, title"

4. Type: "$750,000"
   → Bot updates: price = 750000
   → Bot still shows: "⚠️ Missing: title"

5. Type: "Austin Family Home"
   → Bot shows complete summary
   → All required fields now present
```

### Demo 4: Property Search

**What to show:**
- Natural language search
- Multiple filter criteria
- Results display

**Script:**
```
1. [Click "Search Properties"]

2. Type: "2 bedroom apartment in New York under $700,000 with parking"
   → Bot extracts: rooms=2, city=New York, max_price=700000, parking=true

3. Bot shows: "✅ Found X properties!"
   → Lists matching properties

4. Each property shows:
   - Full details
   - View/Delete buttons
```

### Demo 5: Smart Property Editing

**What to show:**
- Filter-based property selection
- Field-specific updates
- Field deletion

**Script:**
```
1. [Click "✏️ Edit Property"]

2. Bot asks: "Which property would you like to edit?"

3. Type: "apartment in San Francisco"
   → Bot filters user's properties
   → Shows matching properties

4. [Click "✏️ Edit This Property" on one]

5. Type: "Change price to $850,000"
   → Bot updates only price field
   → Other fields unchanged

6. Type: "delete the description"
   → Bot clears description field
   → Sets it to empty/null

7. Bot shows: "✅ Property updated successfully!"
   → Shows updated property
```

### Demo 6: Show All Properties Option

**What to show:**
- Alternative to filtering
- Complete property list

**Script:**
```
1. [Click "✏️ Edit Property"]

2. Bot asks: "Which property would you like to edit?"

3. Type: "show all properties"
   → Bot shows all user's properties
   → Each with edit button

4. [Click "✏️ Edit This Property" on any]

5. Make changes as in Demo 5
```

---

## Recording Tips

### For Video Demo:

1. **Start with overview:**
   - Show project structure
   - Explain key features
   - Show code highlights

2. **Live demonstration:**
   - Start bot in terminal (visible)
   - Open Telegram (visible)
   - Show complete flow

3. **Highlight features:**
   - Goal-first enforcement
   - Voice input
   - Stateful memory
   - Smart editing

4. **Show edge cases:**
   - Incomplete data
   - Field deletion
   - Filter-based editing

### For Screenshots:

**Key screenshots to capture:**
1. Welcome message with goal menu
2. Goal selection warning (when skipping)
3. Property registration flow
4. Voice recognition confirmation
5. Missing fields prompt
6. Confirmation summary
7. Search results
8. Edit property filtering
9. Field deletion confirmation

---

## Sample Test Data

### Complete Properties (for quick testing)

**Property 1:**
```
Luxury downtown condo in San Francisco, South Beach neighborhood, 
980 square feet, 2 bedrooms, 15th floor, built in 2018, 
price $1,350,000, includes parking, elevator, and storage unit.
Address: 88 Fremont Street.
Description: Panoramic bay views, floor-to-ceiling windows, smart home features.
```

**Property 2:**
```
Spacious single-family house in Austin, West Lake Hills, 
3,100 square feet, 4 bedrooms, built in 2012, price $890,000.
Has two-car garage (parking), no elevator, yes storage.
Address: 205 Sycamore Drive.
Description: Open-concept layout, large backyard with deck, quiet cul-de-sac.
```

**Property 3:**
```
Modern townhouse in Seattle, Ballard neighborhood, 
1,450 square feet, 3 bedrooms, built in 2016, price $625,000.
Includes parking and storage.
Description: Recently renovated, energy-efficient, close to downtown.
```

### Incomplete Properties (for testing missing fields)

**Missing area & price:**
```
Modern townhouse in Seattle, Ballard neighborhood. 
Three bedrooms, two and a half bathrooms, built in 2016. 
Includes parking and storage.
```

**Missing property type:**
```
Located in Denver, Cherry Creek, 1450 square feet, 
two bedrooms, 6th floor, built in 2019, price $525,000. 
Elevator is available.
```

**Missing title:**
```
2,400 square feet, 5 bedrooms, price $760,000, built in 2005. 
Address is 413 Maple Avenue, Fairfield. 
Includes parking, no elevator, yes storage.
```

### Edit Commands (for testing editing)

**Change price:**
```
Edit the property in San Francisco priced at $1,350,000.
Change price to $1,400,000.
```

**Delete description:**
```
For the Austin family house, delete the description entirely.
```

**Multiple changes:**
```
Update the Seattle townhouse: change price to $650,000, 
add elevator, and remove storage.
```

---

## Demo Checklist

Before recording/sharing:

- [ ] Bot starts without errors
- [ ] All API keys configured
- [ ] Database file created
- [ ] Goal selection works
- [ ] Text input works
- [ ] Voice input works (if API key available)
- [ ] Property registration works
- [ ] Missing field detection works
- [ ] Search works
- [ ] Edit with filtering works
- [ ] Field deletion works
- [ ] Show all properties works
- [ ] Confirmation flow works
- [ ] Cancel command works

---

## Quick Test Commands

Copy-paste these in Telegram to quickly test:

```
/start
[Click Register Property]
Luxury apartment in New York, Manhattan, 1200 sq ft, 2 bedrooms, $650,000
Modern Manhattan Apartment
confirm

[Click Search Properties]
2 bedroom apartment under $700,000

[Click Edit Property]
apartment in New York
[Click Edit This Property]
Change price to $700,000
```

---

## Expected Results

### Registration Flow:
- Extracts all information correctly
- Detects missing fields
- Shows summary before saving
- Saves to database

### Search Flow:
- Extracts search criteria
- Filters properties correctly
- Shows matching results

### Edit Flow:
- Asks for property criteria
- Filters user's properties
- Updates only specified fields
- Deletes fields when requested

---

**Use this guide to demonstrate all features of the chatbot!**

