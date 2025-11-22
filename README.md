# Real Estate Management Chatbot

A fully interactive Telegram chatbot for managing real estate properties with AI-powered natural language understanding, voice input support, and stateful conversation memory.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://telegram.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-black.svg)](https://platform.openai.com/)

## Features

### Complete Voice Support
Full natural language voice interaction for all operations. Users can register properties, search for listings, edit existing entries, and perform all actions using voice messages. The bot converts speech to text using OpenAI transcription models and processes voice input just like typed text, making the interface accessible and convenient.

### Stateful Conversation Memory
Intelligent memory system that remembers all user inputs across multiple messages. The bot accumulates information incrementally, never asking users to re-enter previously provided data. This allows for natural, conversational interactions where users can provide information gradually without losing context.

### Smart Confirmation Flow
Interactive confirmation system that displays a complete summary of collected information before final submission. Users can review all details, make edits, add missing information, or cancel the operation. This prevents errors and ensures data accuracy.

### Intelligent Information Extraction
Powered by OpenAI GPT-4o, the bot understands natural language input and automatically extracts structured property data from free-form text. It identifies property types, locations, prices, sizes, amenities, and other details without requiring rigid input formats.

### Flexible Property Editing
Advanced editing system that allows users to find properties by describing their characteristics (location, price, type) rather than requiring exact IDs. Users can update specific fields, delete information, or modify multiple attributes in a single operation.

### Lightweight Database
Uses SQLite by default for easy setup and deployment. No external database server required, making it perfect for small to medium-scale deployments. Can be easily upgraded to PostgreSQL or MySQL for production environments.

### Robust Error Handling
Built-in error handling and recovery mechanisms. The bot gracefully handles missing information, invalid inputs, API failures, and other edge cases, providing clear feedback to users and maintaining system stability.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram account
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- OpenAI API Key (from [OpenAI Platform](https://platform.openai.com/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/aeinkoupaei/Real-Estate-Bot.git
cd Real-Estate-Bot
```

2. **Create virtual environment**
```bash
python3 -m venv realassist
source realassist/bin/activate  # On Windows: realassist\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file:
```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o
OPENAI_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
DATABASE_URL=sqlite:///real_estate.db
LOG_LEVEL=INFO
```

5. **Test the setup**
```bash
python test_bot_components.py
```

6. **Run the bot**
```bash
python bot.py
```

## How It Works

### 1. Goal Selection (Required First Step)

When you start the bot, you **must** select a goal:
- Register a property
- Search for properties
- Filter by keyword
- Edit a property
- View my properties

### 2. Natural Language Input

Provide information naturally using **text or voice**:

**Text Example:**
```
User: I have a 2-bedroom apartment in Manhattan, 1000 square feet, $450,000
Bot: Missing: Property title
     I've saved: [shows extracted info]
User: Modern Manhattan Apartment
Bot: Summary: [complete info]
     Confirm?
```

**Voice Example:**
```
User: [Voice] "Two bedroom house in Los Angeles, 1500 square feet, 
     has parking and garage, price $650,000"
Bot: Voice recognized: "Two bedroom house..."
     Processing...
     Summary: [complete info]
```

### 3. Stateful Memory

The bot remembers everything across multiple messages:

```
Message 1: "I have an apartment"
  → Saved: {type: "apartment"}

Message 2: "In New York"
  → Saved: {type: "apartment", city: "New York"}

Message 3: "120 square meters"
  → Saved: {type: "apartment", city: "New York", area: 120}

Bot NEVER asks to re-enter previous information!
```

### 4. Smart Editing

Edit properties by describing what you want to change:

```
User: Edit the property in Manhattan priced at $450,000
Bot: Found 1 property matching your criteria:
     [Shows property]
     Select property to edit

User: [Selects property]
Bot: Tell me what you want to change

User: Change price to $500,000 and delete the description
Bot: Property updated successfully!
```

## Testing & Demo

### Run Component Tests

```bash
python test_bot_components.py
```

This tests:
- Configuration loading
- Database connectivity
- AI handler
- Voice handler
- CRUD operations

### Interactive Demo

1. **Start the bot**
```bash
python bot.py
```

2. **Open Telegram** and find your bot

3. **Try these commands:**
   - `/start` - See welcome message
   - Click "Register Property" - Register a new property
   - Click "Search Properties" - Search for properties
   - Click "Edit Property" - Edit existing properties

4. **Test voice input:**
   - Send a voice message describing a property
   - Bot will convert to text and process

### Sample Test Data

Use these sample property descriptions to test:

**Complete Property:**
```
Luxury downtown condo in San Francisco, South Beach neighborhood, 
980 square feet, 2 bedrooms, 15th floor, built in 2018, 
price $1,350,000, includes parking, elevator, and storage unit.
```

**Incomplete Property (to test missing field detection):**
```
Modern townhouse in Seattle, Ballard neighborhood. 
Three bedrooms, built in 2016. Includes parking and storage.
```
*(Missing: area and price - bot will ask for these)*

**Edit Command:**
```
Edit the property in San Francisco priced at $1,350,000
Change price to $1,400,000 and delete the description
```

## Project Structure

```
Real-Estate-Bot/
├── bot.py                  # Main bot application
├── config.py               # Configuration and messages
├── database.py             # Database models and operations
├── gpt_handler.py          # AI processing
├── voice_handler.py        # Voice processing
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── test_bot_components.py  # Component tests
├── README.md               # This file
├── USAGE_GUIDE.md          # Detailed user guide
├── DEPLOYMENT_GUIDE.md     # Deployment instructions
└── tests/                  # Test suite
```

## Key Features Explained

### Voice Support
Not just voice commands, but **full natural language voice interaction** for all operations. The bot uses OpenAI's transcription models to convert voice messages into text and processes them just like typed messages.

### Smart Memory
Truly remembers conversation context and **never asks to re-enter** information. The bot maintains session state and intelligently merges new information with previously collected data, creating a seamless user experience.

### Interactive Confirmation
Users can **review and edit** before committing, preventing errors. The confirmation flow shows a complete summary, allows field-level edits, and provides clear options to confirm, modify, or cancel.

## Documentation

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete user guide with examples
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment options and instructions
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing procedures
- **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** - Fast deployment guide
- **[DEMO.md](DEMO.md)** - Interactive demo guide

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `OPENAI_MODEL` | GPT model name (default: gpt-4o) | No |
| `OPENAI_TRANSCRIPTION_MODEL` | Whisper/GPT transcription model | No |
| `DATABASE_URL` | Database connection string | No |
| `LOG_LEVEL` | Logging level (INFO, DEBUG, etc.) | No |

### Getting API Keys

**Telegram Bot Token:**
1. Open Telegram
2. Search for [@BotFather](https://t.me/BotFather)
3. Send `/newbot`
4. Follow instructions
5. Copy the token

**OpenAI API Key:**
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Sign in with your OpenAI account
3. Navigate to API Keys and click “Create new secret key”
4. Copy the key and store it securely

## Testing

### Run All Tests

```bash
# Component tests
python test_bot_components.py

# Manual testing
python bot.py
# Then test in Telegram
```

## Troubleshooting

### Bot Not Responding
- Check if goal is selected
- Verify API keys in `.env`
- Check logs for errors

### Voice Not Working
- Verify `OPENAI_API_KEY` is set
- Check internet connection
- Try text input as alternative

### Properties Not Saving
- Check database file permissions
- Verify all required fields provided
- Check terminal for error messages

## Acknowledgments

- **OpenAI** for advanced GPT and Whisper capabilities
- **python-telegram-bot** - Excellent Telegram bot framework
- **SQLAlchemy** - Robust ORM for database operations

## Support

- Check [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed instructions
- Open an issue on GitHub for bugs
- Suggest features via GitHub issues

## Features Showcase

### Example Conversation Flow

```
User: /start
Bot: Welcome! Please select your goal:
     [Menu with options]

User: [Clicks "Register Property"]
Bot: Register a New Property
     Please provide the property details...

User: [Voice] "Two bedroom apartment in Manhattan, 
     1000 square feet, 5th floor, has parking, $450,000"

Bot: Voice recognized: "Two bedroom apartment..."
     Missing: Property title
     I've saved: [shows extracted info]

User: Modern Manhattan Apartment

Bot: Summary: [complete information]
     Confirm?

User: confirm

Bot: Your property has been successfully registered!
     [Shows property details]
```

