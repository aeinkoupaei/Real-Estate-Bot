"""
Real Estate Bot Configuration File
This file contains all configuration settings, messages, and prompts for the bot.
All text is in English as per requirements.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')
OPENAI_TRANSCRIPTION_MODEL = os.getenv('OPENAI_TRANSCRIPTION_MODEL', 'gpt-4o-mini-transcribe')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///real_estate.db')

# Administrative Settings
BOT_ADMIN_IDS = [int(id_) for id_ in os.getenv('BOT_ADMIN_IDS', '').split(',') if id_.strip()]
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Bot Messages in English
MESSAGES = {
    'welcome': """
🏠 Welcome to the Real Estate Management Chatbot!

I'm your intelligent assistant for managing property information, powered by OpenAI GPT-4o. 🤖

**Please select your goal first:**
• Register a property
• Search for a property
• Filter properties by keyword
• Edit a property
• View my properties

You can select from the menu below or type your goal directly.

💬 **Both text and voice input are supported!**
""",
    'select_goal': """
❓ Please specify your goal first. What would you like to do?

Choose one of the following options:
• Register a property
• Search for a property  
• Filter properties by keyword
• Edit a property
• View my properties

You can type your choice or select from the menu below. 👇
""",
    'help': """
📚 How to Use This Bot:

**Available Commands:**
/start - Start the bot and select your goal
/cancel - Cancel current operation
/help - Show this help message

**How It Works:**
1. First, select your goal (Register, Search, Filter, or Edit)
2. Provide information step by step (text or voice)
3. I'll remember everything you've told me
4. Review and confirm before submitting
5. You can cancel or edit at any time

**Voice Support:**
You can use voice input for ALL interactions! Just send a voice message instead of typing.

**Smart Memory:**
I remember all your previous inputs, so you only need to provide missing or updated information.
""",
    'register_start': """
📝 Register a New Property

Please provide the property details. You can:
• Type the information
• Send a voice message
• Provide details step by step

**Example:**
"A 120 square meter apartment in New York, 2 bedrooms, 3rd floor, price $500,000"

I'll remember everything you tell me. You can add more details in multiple messages.

**Required information:**
- Property type (apartment, house, land, etc.)
- Location (city and neighborhood)
- Size (square meters or square feet)
- Price
- Number of rooms/bedrooms

**Optional details:**
- Floor number
- Year built
- Parking availability
- Elevator
- Storage room
- Any additional description

Send your information now, or type /cancel to stop.
""",
    'search_start': """
🔍 Search for Properties

Please describe what kind of property you're looking for. You can:
• Type your requirements
• Send a voice message describing what you need

**Search by:**
• Location (city or neighborhood)
• Size (e.g., "between 80 and 120 square meters")
• Price range (e.g., "under $400,000")
• Number of bedrooms
• Property type (apartment, house, villa, land)
• Amenities (parking, elevator, etc.)

**Example:**
"2-bedroom apartment in downtown, price under $500,000, with parking"

Send your search criteria now, or type /cancel to stop.
""",
    'filter_start': """
🔎 Filter Properties by Keyword

Enter keywords to search through all property descriptions and details.

**Examples:**
• "luxury penthouse"
• "garden"
• "newly renovated"
• "near subway"

Send your keywords now, or type /cancel to stop.
""",
    'edit_start': """
✏️ Edit a Property

First, tell me which property you want to edit.
• Describe it (for example: "apartment in Boston under $600,000")
• Or type "show all properties" to list everything

Once I show matching properties, pick the one you want to edit.
""",
    'edit_need_filters': """
⚠️ I did not catch any property details.

Please describe the property you want to edit (city, price, size, etc.),
or type "show all properties" to see your entire list.
""",
    'edit_no_matches': """
😔 I could not find any of your properties matching that description.

Please refine the details or type "show all properties" to view everything.
""",
    'edit_results_header': "✅ I found {count} properties that match your description. Pick one below to start editing:",
    'edit_results_more': "📌 {remaining} additional properties are available. Refine your filters to narrow the list.",
    'edit_all_listed': """
📋 Here are all of your properties.

Tap the button under the property you want to edit.
""",
    'edit_select_prompt': "Select a property to edit, then tell me what to change (text or voice both work). You can also describe another property or type \"show all properties\" if you want to refine the list.",
    'missing_info': """
⚠️ Some information is missing:

{missing_fields}

Please provide the missing details. I've already saved:
{saved_info}

You can type or send a voice message with the missing information.
""",
    'confirm_data': """
✅ Here's the information I have collected:

{summary}

Would you like to:
• **Confirm and submit** - Type "confirm" or "yes"
• **Add/Edit information** - Just tell me what to change
• **Cancel** - Type "cancel" or /cancel

What would you like to do?
""",
    'success_register': """
✅ Your property has been successfully registered!

{property_details}

What would you like to do next?
""",
    'success_search': """
🔍 Search Results:

Found {count} properties matching your criteria:

{results}

Would you like to refine your search or start a new task?
""",
    'cancel': """
❌ Operation cancelled.

What would you like to do next?
""",
    'error': 'An error occurred. Please try again.',
    'voice_recognized': """
🎤 Voice recognized:
"{text}"

Processing your request...
""",
    'no_goal_warning': """
⚠️ Please specify your goal first. What would you like to do?

Select an option from the menu below:
""",
}

# AI Prompts for Property Information Extraction
PROPERTY_EXTRACTION_PROMPT = """
You are an intelligent assistant for extracting property information.
Extract property details from the user's input text and return them in JSON format.

Required fields:
- title: property title
- property_type: type of property (apartment, house, villa, land, shop, etc.)
- city: city name
- neighborhood: neighborhood or district
- address: full address
- area: size in square meters or square feet (number)
- price: price (number)
- rooms: number of bedrooms (number)
- floor: floor number (number or null)
- year_built: year of construction (number or null)
- parking: parking availability (true/false)
- elevator: elevator availability (true/false)
- storage: storage room availability (true/false)
- description: additional description

If information is not specified, set the value to null.
Return ONLY the JSON object, without any additional explanation.
"""

SEARCH_QUERY_PROMPT = """
You are an intelligent assistant for converting search requests into database filters.
Extract search criteria from the user's input text and return them in JSON format.

Searchable fields:
- property_type: type of property
- city: city name
- neighborhood: neighborhood or district
- min_area: minimum size
- max_area: maximum size
- min_price: minimum price
- max_price: maximum price
- rooms: number of bedrooms
- parking: parking required (true/false/null)
- elevator: elevator required (true/false/null)

Return ONLY the JSON object, without any additional explanation.
"""

