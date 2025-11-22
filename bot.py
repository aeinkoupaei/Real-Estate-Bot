"""
Real Estate Management Telegram Bot
A fully interactive chatbot with goal-first approach, voice support, and stateful memory.
All messages and code comments are in English.
"""
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from database import DatabaseManager
from gpt_handler import GptHandler
from voice_handler import VoiceHandler
import config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

# Conversation states - these define where the user is in the conversation flow
STATE_WAITING_FOR_GOAL = 'waiting_for_goal'
STATE_REGISTER = 'registering'
STATE_SEARCH = 'searching'
STATE_FILTER = 'filtering'
STATE_EDIT_FILTER = 'edit_filtering'
STATE_EDIT_SELECTION = 'edit_selecting'
STATE_EDIT = 'editing'
STATE_CONFIRM = 'confirming'

# Global handlers for database, AI, and voice processing
db_manager = DatabaseManager()
gpt_handler = GptHandler()
voice_handler = VoiceHandler()


class RealEstateBot:
    """
    Main bot class for real estate management.
    Implements goal-first approach with full voice support and stateful memory.
    """
    
    def __init__(self):
        """Initialize the bot with database and AI handlers"""
        self.db = db_manager
        self.ai = gpt_handler
    
    # ========================
    # Command Handlers
    # ========================
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command - Entry point for the bot
        Shows welcome message and asks user to select their goal first
        """
        # Reset user state to ensure clean start
        context.user_data.clear()
        context.user_data['state'] = STATE_WAITING_FOR_GOAL
        
        await update.message.reply_text(
            config.MESSAGES['welcome'],
            reply_markup=self._get_goal_selection_keyboard()
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command - Show usage instructions"""
        await update.message.reply_text(config.MESSAGES['help'])
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /cancel command - Cancel current operation and return to goal selection
        User can restart the process at any time
        """
        # Clear all user data except basic info
        context.user_data.clear()
        context.user_data['state'] = STATE_WAITING_FOR_GOAL
        
        await update.message.reply_text(
            config.MESSAGES['cancel'],
            reply_markup=self._get_goal_selection_keyboard()
        )
    
    # ========================
    # Goal Selection Handlers
    # ========================
    
    async def handle_goal_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, goal: str):
        """
        Handle goal selection from inline keyboard buttons
        This is called when user clicks one of the goal buttons
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            goal: Selected goal (register/search/filter/edit/list)
        """
        query = update.callback_query
        await query.answer()
        
        # Set the user's goal and initialize data storage
        context.user_data['goal'] = goal
        context.user_data['partial_data'] = {}  # Store accumulated property data
        context.user_data['conversation_history'] = []  # Track conversation for context
        
        if goal == 'register':
            context.user_data['state'] = STATE_REGISTER
            await query.message.reply_text(config.MESSAGES['register_start'])
            
        elif goal == 'search':
            context.user_data['state'] = STATE_SEARCH
            await query.message.reply_text(config.MESSAGES['search_start'])
            
        elif goal == 'filter':
            context.user_data['state'] = STATE_FILTER
            await query.message.reply_text(config.MESSAGES['filter_start'])
            
        elif goal == 'edit':
            context.user_data['state'] = STATE_EDIT_FILTER
            await query.message.reply_text(config.MESSAGES['edit_start'])
            
        elif goal == 'list':
            # Show user's properties
            await self.show_user_properties(update, context, for_editing=False)
            # Return to goal selection after showing list
            context.user_data['state'] = STATE_WAITING_FOR_GOAL
    
    # ========================
    # Message Handlers
    # ========================
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle all text messages from the user
        This is the main text input handler that processes user messages based on current state
        """
        user_message = update.message.text
        current_state = context.user_data.get('state', STATE_WAITING_FOR_GOAL)
        
        # CRITICAL REQUIREMENT: If no goal is set, force user to select a goal first
        if current_state == STATE_WAITING_FOR_GOAL or not context.user_data.get('goal'):
            # Check if user is trying to select a goal by typing it
            goal = self._parse_goal_from_text(user_message)
            if goal:
                # Create a fake callback query to reuse goal selection logic
                await self._handle_text_goal_selection(update, context, goal)
            else:
                # User didn't specify a valid goal, show warning
                await update.message.reply_text(
                    config.MESSAGES['no_goal_warning'],
                    reply_markup=self._get_goal_selection_keyboard()
                )
            return
        
        # Process message based on current state
        if current_state == STATE_REGISTER:
            await self.process_register_input(update, context, user_message)
            
        elif current_state == STATE_SEARCH:
            await self.process_search_input(update, context, user_message)
            
        elif current_state == STATE_FILTER:
            await self.process_filter_input(update, context, user_message)
            
        elif current_state in [STATE_EDIT_FILTER, STATE_EDIT_SELECTION]:
            await self.process_edit_filter_input(update, context, user_message)
            
        elif current_state == STATE_EDIT:
            await self.process_edit_input(update, context, user_message)
            
        elif current_state == STATE_CONFIRM:
            await self.process_confirmation(update, context, user_message)
    
    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle voice messages from the user.
        Converts voice to text using OpenAI's transcription API, then processes like text input.
        Voice input is supported for ALL major actions.
        """
        current_state = context.user_data.get('state', STATE_WAITING_FOR_GOAL)
        
        # Check if voice service is available
        if not voice_handler.is_available():
            await update.message.reply_text(
                "❌ Voice service is currently unavailable.\n\n"
                "Please make sure:\n"
                "1. OPENAI_API_KEY is configured in .env\n"
                "2. You have restarted the bot\n"
                "3. VPN is active if needed\n\n"
                "You can continue using text input."
            )
            return
        
        # Show processing message
        processing_msg = await update.message.reply_text("🎤 Converting voice to text...")
        
        try:
            # Download voice file from Telegram
            voice_file = await update.message.voice.get_file()
            voice_path = f"voice_{update.effective_user.id}_{update.message.message_id}.ogg"
            await voice_file.download_to_drive(voice_path)
            
            # Convert voice to text using OpenAI
            text = await voice_handler.voice_to_text(voice_path)
            
            # Clean up: delete the voice file
            os.remove(voice_path)
            
            if not text:
                await processing_msg.edit_text(
                    "❌ Could not recognize the voice clearly.\n"
                    "Please try again or use text input."
                )
                return
            
            # Show recognized text to user for confirmation
            await processing_msg.edit_text(
                config.MESSAGES['voice_recognized'].format(text=text)
            )
            
            # CRITICAL: Check if user has selected a goal
            if current_state == STATE_WAITING_FOR_GOAL or not context.user_data.get('goal'):
                # Try to parse goal from voice input
                goal = self._parse_goal_from_text(text)
                if goal:
                    await self._handle_text_goal_selection(update, context, goal)
                else:
                    await update.message.reply_text(
                        config.MESSAGES['no_goal_warning'],
                        reply_markup=self._get_goal_selection_keyboard()
                    )
                return
            
            # Process the recognized text based on current state
            if current_state == STATE_REGISTER:
                await self.process_register_input(update, context, text)
                
            elif current_state == STATE_SEARCH:
                await self.process_search_input(update, context, text)
                
            elif current_state == STATE_FILTER:
                await self.process_filter_input(update, context, text)
                
            elif current_state in [STATE_EDIT_FILTER, STATE_EDIT_SELECTION]:
                await self.process_edit_filter_input(update, context, text)
                
            elif current_state == STATE_EDIT:
                await self.process_edit_input(update, context, text)
                
            elif current_state == STATE_CONFIRM:
                await self.process_confirmation(update, context, text)
        
        except Exception as e:
            logger.error(f"Error processing voice: {e}")
            await processing_msg.edit_text(
                "❌ An error occurred while processing your voice message.\n"
                "Please try again or use text input."
            )
    
    # ========================
    # Input Processing Methods
    # ========================
    
    async def process_register_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
        """
        Process input for property registration
        Extracts property information and merges with previously saved data
        Only asks for missing information, never requires re-entering everything
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            user_input: User's text or voice-to-text input
        """
        user_id = update.effective_user.id
        
        # Add to conversation history for context
        context.user_data['conversation_history'].append({
            'role': 'user',
            'message': user_input
        })
        
        # Show processing message
        processing_msg = await update.message.reply_text("⏳ Processing your information...")
        
        # Extract property information using AI
        new_data = self.ai.extract_property_info(user_input)
        
        if not new_data:
            await processing_msg.edit_text(
                "❌ I couldn't understand the property information.\n"
                "Please provide the details more clearly.\n\n"
                "Example: 120 square meter apartment in New York, 2 bedrooms, price $500,000"
            )
            return
        
        # CRITICAL: Merge with existing partial data (stateful memory)
        # This ensures we never lose previously entered information
        partial_data = context.user_data.get('partial_data', {})
        merged_data = {**partial_data, **new_data}  # New data overwrites old if keys match
        context.user_data['partial_data'] = merged_data
        
        # Validate: check if all required fields are present
        is_valid, missing_fields, validated_data = self.ai.validate_property_data(merged_data)
        
        if not is_valid:
            # Show what we have so far and ask for missing information
            saved_info = self._format_property_summary(merged_data)
            missing_list = self._format_missing_fields(missing_fields)
            
            message = config.MESSAGES['missing_info'].format(
                missing_fields=missing_list,
                saved_info=saved_info
            )
            await processing_msg.edit_text(message)
            return
        
        # All required data is present - show confirmation
        context.user_data['state'] = STATE_CONFIRM
        summary = self._format_property_summary(validated_data)
        
        message = config.MESSAGES['confirm_data'].format(summary=summary)
        await processing_msg.edit_text(message)
    
    async def process_search_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
        """
        Process input for property search
        Extracts search filters and performs database query
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            user_input: User's search criteria
        """
        # Add to conversation history
        context.user_data['conversation_history'].append({
            'role': 'user',
            'message': user_input
        })
        
        # Show processing message
        processing_msg = await update.message.reply_text("🔍 Searching for properties...")
        
        # Extract search filters using AI
        filters = self.ai.extract_search_filters(user_input)
        
        # Merge with any previously set filters (stateful)
        existing_filters = context.user_data.get('partial_data', {})
        merged_filters = {**existing_filters, **filters}
        context.user_data['partial_data'] = merged_filters
        
        # Search in database
        properties = self.db.search_properties(merged_filters)
        
        # Display results
        if not properties:
            await processing_msg.edit_text(
                "😔 No properties found matching your criteria.\n\n"
                "Try:\n"
                "• Broadening your search criteria\n"
                "• Removing some filters\n"
                "• Searching in a different location"
            )
            # Return to goal selection
            context.user_data['state'] = STATE_WAITING_FOR_GOAL
            await update.message.reply_text(
                "What would you like to do next?",
                reply_markup=self._get_goal_selection_keyboard()
            )
            return
        
        # Show summary
        count = len(properties)
        await processing_msg.edit_text(f"✅ Found {count} properties!")
        
        # Show each property (limit to 10 to avoid flooding)
        for prop in properties[:10]:
            await update.message.reply_text(
                prop.to_text(),
                reply_markup=self._get_property_actions_keyboard(prop.id, False)
            )
        
        if len(properties) > 10:
            await update.message.reply_text(
                f"📌 {len(properties) - 10} more properties found.\n"
                "Please refine your search to see more specific results."
            )
        
        # Return to goal selection
        context.user_data['state'] = STATE_WAITING_FOR_GOAL
        await update.message.reply_text(
            "Search complete! What would you like to do next?",
            reply_markup=self._get_goal_selection_keyboard()
        )
    
    async def process_filter_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
        """
        Process keyword-based filtering
        Searches through all property fields using keywords
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            user_input: Keywords to search for
        """
        processing_msg = await update.message.reply_text("🔎 Filtering properties...")
        
        # Search by keywords in description and other text fields
        properties = self.db.filter_by_keywords(user_input)
        
        if not properties:
            await processing_msg.edit_text(
                f"😔 No properties found with keywords: '{user_input}'\n\n"
                "Try different keywords or start a new search."
            )
        else:
            count = len(properties)
            await processing_msg.edit_text(f"✅ Found {count} properties matching your keywords!")
            
            for prop in properties[:10]:
                await update.message.reply_text(
                    prop.to_text(),
                    reply_markup=self._get_property_actions_keyboard(prop.id, False)
                )
        
        # Return to goal selection
        context.user_data['state'] = STATE_WAITING_FOR_GOAL
        await update.message.reply_text(
            "What would you like to do next?",
            reply_markup=self._get_goal_selection_keyboard()
        )
    
    async def process_edit_filter_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
        """
        Process filter instructions for editing properties
        Allows user to narrow down which property they want to edit before selecting it
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            user_input: Filter criteria or commands (e.g., "show all properties")
        """
        user_id = update.effective_user.id
        text = user_input.strip()
        lower_text = text.lower()
        
        show_all_keywords = [
            "show all properties",
            "show all",
            "list all properties",
            "see all properties",
            "display all properties"
        ]
        
        # Handle request to show every property
        if any(phrase in lower_text for phrase in show_all_keywords):
            properties = self.db.get_user_properties(user_id)
            
            if not properties:
                await update.message.reply_text(
                    "You have not registered any properties yet. Add one first, then come back to edit it."
                )
                context.user_data['state'] = STATE_WAITING_FOR_GOAL
                await update.message.reply_text(
                    "What would you like to do next?",
                    reply_markup=self._get_goal_selection_keyboard()
                )
                return
            
            await update.message.reply_text(config.MESSAGES['edit_all_listed'].strip())
            await self._send_properties_for_editing(update, context, properties)
            context.user_data['state'] = STATE_EDIT_SELECTION
            return
        
        # Extract filters using AI
        filters = self.ai.extract_search_filters(user_input)
        
        if not filters:
            await update.message.reply_text(config.MESSAGES['edit_need_filters'].strip())
            return
        
        filters['user_id'] = user_id
        context.user_data['latest_edit_filters'] = filters
        
        properties = self.db.search_properties(filters)
        
        if not properties:
            await update.message.reply_text(config.MESSAGES['edit_no_matches'].strip())
            return
        
        await update.message.reply_text(
            config.MESSAGES['edit_results_header'].format(count=len(properties))
        )
        await self._send_properties_for_editing(update, context, properties)
        context.user_data['state'] = STATE_EDIT_SELECTION
    
    async def process_edit_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
        """
        Process input for editing an existing property
        Updates only the specified fields, keeps other data unchanged
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            user_input: Update information
        """
        property_id = context.user_data.get('editing_property_id')
        
        if not property_id:
            await update.message.reply_text(
                "⚠️ Please select a property to edit first."
            )
            return
        
        processing_msg = await update.message.reply_text("⏳ Processing updates...")
        
        # Extract update information
        updates = self.ai.extract_property_info(user_input) or {}
        deletion_updates = self._detect_field_deletions(user_input)
        
        if deletion_updates:
            updates.update(deletion_updates)
        
        if not updates:
            await processing_msg.edit_text(
                "❌ I couldn't understand what you want to change.\n"
                "Please specify clearly what to update.\n\n"
                "Examples:\n"
                "• \"Change price to $550,000 and add parking\"\n"
                "• \"Delete the description\""
            )
            return
        
        # Update the property in database
        success = self.db.update_property(property_id, updates)
        
        if success:
            # Get updated property
            updated_prop = self.db.get_property(property_id)
            await processing_msg.edit_text(
                "✅ Property updated successfully!\n\n" + updated_prop.to_text()
            )
        else:
            await processing_msg.edit_text("❌ Failed to update property.")
        
        # Return to goal selection
        context.user_data.pop('editing_property_id', None)
        context.user_data.pop('available_edit_property_ids', None)
        context.user_data['state'] = STATE_WAITING_FOR_GOAL
        await update.message.reply_text(
            "What would you like to do next?",
            reply_markup=self._get_goal_selection_keyboard()
        )
    
    async def process_confirmation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_input: str):
        """
        Process user's confirmation response
        Handles: confirm/yes to submit, any other text to add/edit info, cancel to abort
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            user_input: User's confirmation response
        """
        user_input_lower = user_input.lower().strip()
        
        # Check if user wants to confirm and submit
        if any(word in user_input_lower for word in ['confirm', 'yes', 'submit', 'ok', 'correct', 'save']):
            await self.finalize_registration(update, context)
            
        # Check if user wants to cancel
        elif any(word in user_input_lower for word in ['cancel', 'no', 'abort', 'stop']):
            await self.cancel(update, context)
            
        # User wants to add or edit information
        else:
            # Process as additional/update information
            await update.message.reply_text("📝 Updating information...")
            
            # Extract new/updated information
            new_data = self.ai.extract_property_info(user_input)
            
            if new_data:
                # Merge with existing data
                partial_data = context.user_data.get('partial_data', {})
                merged_data = {**partial_data, **new_data}
                context.user_data['partial_data'] = merged_data
                
                # Validate again
                is_valid, missing_fields, validated_data = self.ai.validate_property_data(merged_data)
                
                # Show updated summary
                summary = self._format_property_summary(merged_data)
                message = config.MESSAGES['confirm_data'].format(summary=summary)
                await update.message.reply_text(message)
            else:
                await update.message.reply_text(
                    "❌ I couldn't understand the update.\n"
                    "Please specify what you'd like to change clearly."
                )
    
    async def finalize_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Finalize property registration by saving to database
        Called after user confirms the information
        
        Args:
            update: Telegram update object
            context: Bot context with user data
        """
        user_id = update.effective_user.id
        property_data = context.user_data.get('partial_data', {})
        
        try:
            # Save to database
            property_id = self.db.add_property(user_id, property_data)
            
            # Retrieve saved property
            saved_property = self.db.get_property(property_id)
            
            # Show success message
            await update.message.reply_text(
                config.MESSAGES['success_register'].format(
                    property_details=saved_property.to_text()
                ),
                reply_markup=self._get_property_actions_keyboard(property_id, True)
            )
            
            # Clear state and return to goal selection
            context.user_data.clear()
            context.user_data['state'] = STATE_WAITING_FOR_GOAL
            
            await update.message.reply_text(
                "What would you like to do next?",
                reply_markup=self._get_goal_selection_keyboard()
            )
            
        except Exception as e:
            logger.error(f"Error saving property: {e}")
            await update.message.reply_text(
                "❌ An error occurred while saving the property.\n"
                "Please try again."
            )
    
    # ========================
    # Helper Methods
    # ========================
    
    async def show_user_properties(self, update: Update, context: ContextTypes.DEFAULT_TYPE, for_editing: bool):
        """
        Show list of user's properties
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            for_editing: If True, prepare properties for editing; if False, just display
        """
        user_id = update.effective_user.id
        query = update.callback_query
        
        properties = self.db.get_user_properties(user_id)
        
        if not properties:
            message = (
                "You haven't registered any properties yet.\n\n"
                "Would you like to register one now?"
            )
            if query:
                await query.message.reply_text(message)
            else:
                await update.message.reply_text(message)
            return []
        
        if for_editing:
            target_message = query.message if query else update.message
            await target_message.reply_text(config.MESSAGES['edit_all_listed'].strip())
            await self._send_properties_for_editing(update, context, properties)
            return properties
        
        message = f"📋 You have {len(properties)} properties:\n\n"
        target_message = query.message if query else update.message
        await target_message.reply_text(message)
        
        for prop in properties:
            keyboard = self._get_property_actions_keyboard(prop.id, True, for_editing=False)
            await target_message.reply_text(prop.to_text(), reply_markup=keyboard)
        
        return properties

    async def _send_properties_for_editing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, properties, limit: int = 10):
        """
        Helper method to send property cards with edit buttons
        
        Args:
            update: Telegram update object
            context: Bot context
            properties: Iterable of Property objects
            limit: Maximum number of property cards to show at once
        """
        if not properties:
            return
        
        # Store available property IDs for validation later
        context.user_data['available_edit_property_ids'] = [prop.id for prop in properties]
        
        target_message = update.callback_query.message if update.callback_query else update.message
        
        for prop in properties[:limit]:
            await target_message.reply_text(
                prop.to_text(),
                reply_markup=self._get_property_actions_keyboard(prop.id, True, for_editing=True)
            )
        
        if len(properties) > limit:
            await target_message.reply_text(
                config.MESSAGES['edit_results_more'].format(remaining=len(properties) - limit)
            )
        
        await target_message.reply_text(config.MESSAGES['edit_select_prompt'])
    
    def _parse_goal_from_text(self, text: str) -> str:
        """
        Parse goal from user's text input
        Detects keywords to identify which goal the user wants
        
        Args:
            text: User's input text
            
        Returns:
            Goal string (register/search/filter/edit/list) or None
        """
        text_lower = text.lower()
        
        # Keywords for each goal
        register_keywords = ['register', 'add', 'create', 'new property', 'list property', 'post']
        search_keywords = ['search', 'find', 'look for', 'looking for', 'want to find']
        filter_keywords = ['filter', 'keyword', 'contains']
        edit_keywords = ['edit', 'update', 'modify', 'change']
        list_keywords = ['list', 'show my', 'my properties', 'view my']
        
        if any(keyword in text_lower for keyword in register_keywords):
            return 'register'
        elif any(keyword in text_lower for keyword in search_keywords):
            return 'search'
        elif any(keyword in text_lower for keyword in filter_keywords):
            return 'filter'
        elif any(keyword in text_lower for keyword in edit_keywords):
            return 'edit'
        elif any(keyword in text_lower for keyword in list_keywords):
            return 'list'
        
        return None
    
    async def _handle_text_goal_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, goal: str):
        """
        Handle goal selection when user types their goal instead of clicking a button
        
        Args:
            update: Telegram update object
            context: Bot context with user data
            goal: Detected goal
        """
        context.user_data['goal'] = goal
        context.user_data['partial_data'] = {}
        context.user_data['conversation_history'] = []
        
        if goal == 'register':
            context.user_data['state'] = STATE_REGISTER
            await update.message.reply_text(config.MESSAGES['register_start'])
            
        elif goal == 'search':
            context.user_data['state'] = STATE_SEARCH
            await update.message.reply_text(config.MESSAGES['search_start'])
            
        elif goal == 'filter':
            context.user_data['state'] = STATE_FILTER
            await update.message.reply_text(config.MESSAGES['filter_start'])
            
        elif goal == 'edit':
            context.user_data['state'] = STATE_EDIT
            await self.show_user_properties(update, context, for_editing=True)
            
        elif goal == 'list':
            await self.show_user_properties(update, context, for_editing=False)
            context.user_data['state'] = STATE_WAITING_FOR_GOAL
    
    def _format_property_summary(self, property_data: dict) -> str:
        """
        Format property data into a readable summary
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            Formatted string summary
        """
        summary = []
        
        field_labels = {
            'title': '🏠 Title',
            'property_type': '🏢 Type',
            'city': '🌆 City',
            'neighborhood': '📍 Neighborhood',
            'address': '📮 Address',
            'area': '📐 Area',
            'price': '💰 Price',
            'rooms': '🛏 Bedrooms',
            'floor': '🏗 Floor',
            'year_built': '📅 Year Built',
            'parking': '🅿️ Parking',
            'elevator': '🛗 Elevator',
            'storage': '📦 Storage',
            'description': '📝 Description'
        }
        
        for key, label in field_labels.items():
            if key in property_data and property_data[key] not in [None, '', 'null']:
                value = property_data[key]
                
                # Format boolean values
                if isinstance(value, bool):
                    value = 'Yes' if value else 'No'
                
                # Format numbers with commas
                elif key in ['price', 'area'] and isinstance(value, (int, float)):
                    value = f"{value:,.2f}"
                
                summary.append(f"{label}: {value}")
        
        return '\n'.join(summary) if summary else "No information collected yet."
    
    def _format_missing_fields(self, missing_fields: list) -> str:
        """
        Format list of missing fields into readable text
        
        Args:
            missing_fields: List of field names that are missing
            
        Returns:
            Formatted string listing missing fields
        """
        field_names = {
            'title': 'Property title',
            'property_type': 'Property type (apartment, house, etc.)',
            'city': 'City',
            'neighborhood': 'Neighborhood',
            'area': 'Size/Area',
            'price': 'Price',
            'rooms': 'Number of bedrooms'
        }
        
        formatted = [f"• {field_names.get(f, f)}" for f in missing_fields]
        return '\n'.join(formatted)
    
    def _detect_field_deletions(self, text: str) -> dict:
        """
        Detect explicit delete/clear commands inside the user's message
        Supports phrases like "delete the description" or "remove parking"
        
        Args:
            text: Raw user input
            
        Returns:
            Dictionary mapping field names to None/False to reflect removals
        """
        if not text:
            return {}
        
        deletion_keywords = ['delete', 'remove', 'clear', 'erase', 'drop']
        reset_keywords = ['set', 'make']
        negative_keywords = ['no', 'without']
        
        field_synonyms = {
            'description': ['description', 'details', 'summary', 'notes', 'note'],
            'address': ['address', 'location details'],
            'neighborhood': ['neighborhood', 'district', 'area name'],
            'title': ['title', 'headline'],
            'parking': ['parking', 'garage', 'car park'],
            'elevator': ['elevator', 'lift'],
            'storage': ['storage', 'storage room', 'locker', 'pantry']
        }
        boolean_fields = {'parking', 'elevator', 'storage'}
        
        normalized = ' '.join(text.lower().split())
        removals = {}
        
        for field, synonyms in field_synonyms.items():
            for synonym in synonyms:
                # Direct deletion commands (delete/remove/clear ...)
                for keyword in deletion_keywords:
                    patterns = [
                        f"{keyword} {synonym}",
                        f"{keyword} the {synonym}",
                        f"{keyword} this {synonym}",
                        f"{keyword} that {synonym}",
                        f"{keyword} my {synonym}",
                        f"{keyword} the {synonym} field"
                    ]
                    if any(pattern in normalized for pattern in patterns):
                        removals[field] = False if field in boolean_fields else None
                        break  # No need to check other keywords for this synonym
                if field in removals:
                    continue
                
                # Reset commands (set description to none/null/empty)
                for keyword in reset_keywords:
                    patterns = [
                        f"{keyword} {synonym} to none",
                        f"{keyword} {synonym} to null",
                        f"{keyword} {synonym} to empty",
                        f"{keyword} {synonym} to blank",
                        f"{keyword} the {synonym} to none",
                        f"{keyword} the {synonym} to null"
                    ]
                    if any(pattern in normalized for pattern in patterns):
                        removals[field] = False if field in boolean_fields else None
                        break
                if field in removals:
                    continue
                
                # Negative phrases for booleans (no parking / without elevator)
                if field in boolean_fields:
                    patterns = [
                        f"{negative_keywords[0]} {synonym}",
                        f"{negative_keywords[1]} {synonym}",
                        f"there is {negative_keywords[0]} {synonym}",
                        f"{synonym} is not needed",
                        f"{synonym} not needed"
                    ]
                    if any(pattern in normalized for pattern in patterns):
                        removals[field] = False
                        continue
        
        return removals
    
    def _get_goal_selection_keyboard(self):
        """
        Create inline keyboard for goal selection
        This is the main menu that appears when user needs to select their goal
        
        Returns:
            InlineKeyboardMarkup with goal options
        """
        keyboard = [
            [
                InlineKeyboardButton("🏠 Register Property", callback_data='goal_register'),
                InlineKeyboardButton("🔍 Search Properties", callback_data='goal_search')
            ],
            [
                InlineKeyboardButton("🔎 Filter by Keyword", callback_data='goal_filter'),
                InlineKeyboardButton("✏️ Edit Property", callback_data='goal_edit')
            ],
            [
                InlineKeyboardButton("📋 My Properties", callback_data='goal_list'),
                InlineKeyboardButton("❓ Help", callback_data='goal_help')
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def _get_property_actions_keyboard(self, property_id: int, is_owner: bool, for_editing: bool = False):
        """
        Create inline keyboard for property actions
        
        Args:
            property_id: ID of the property
            is_owner: Whether current user owns this property
            for_editing: Whether this keyboard is for selecting property to edit
            
        Returns:
            InlineKeyboardMarkup with appropriate action buttons
        """
        keyboard = []
        
        if for_editing:
            # Button to select this property for editing
            keyboard.append([
                InlineKeyboardButton("✏️ Edit This Property", callback_data=f'edit_{property_id}')
            ])
        elif is_owner:
            # Owner can view details or delete
            keyboard.append([
                InlineKeyboardButton("👁 View Details", callback_data=f'view_{property_id}'),
                InlineKeyboardButton("🗑 Delete", callback_data=f'delete_{property_id}')
            ])
        else:
            # Non-owner can only view
            keyboard.append([
                InlineKeyboardButton("👁 View Details", callback_data=f'view_{property_id}')
            ])
        
        return InlineKeyboardMarkup(keyboard)
    
    # ========================
    # Callback Query Handlers
    # ========================
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle all inline keyboard button callbacks
        Routes different callback types to appropriate handlers
        """
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        # Goal selection callbacks
        if data.startswith('goal_'):
            goal = data.replace('goal_', '')
            if goal == 'help':
                await query.message.reply_text(config.MESSAGES['help'])
            else:
                await self.handle_goal_selection(update, context, goal)
        
        # Property action callbacks
        elif data.startswith('view_'):
            await self.view_property(update, context)
        
        elif data.startswith('delete_'):
            await self.delete_property(update, context)
        
        elif data.startswith('confirm_delete_'):
            await self.confirm_delete(update, context)
        
        elif data.startswith('edit_'):
            # Set property for editing
            property_id = int(data.split('_')[1])
            property_obj = self.db.get_property(property_id)
            allowed_ids = context.user_data.get('available_edit_property_ids')
            
            if not property_obj or property_obj.user_id != update.effective_user.id:
                await query.message.reply_text(
                    "❌ You can edit only your own properties. Please pick one from the list I showed you."
                )
                return
            
            if allowed_ids and property_id not in allowed_ids:
                await query.message.reply_text(
                    "⚠️ That property was not in the latest results. Please describe the property again or type \"show all properties\"."
                )
                return
            
            context.user_data['editing_property_id'] = property_id
            context.user_data['state'] = STATE_EDIT
            
            await query.message.reply_text(
                f"✏️ Editing property #{property_id}\n\n"
                "Tell me what you want to change (you can use text or voice).\n\n"
                "Examples:\n"
                "• \"Change price to $600,000\"\n"
                "• \"Remove the description\"\n"
                "• \"Add elevator and parking\""
            )
    
    async def view_property(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """View detailed information about a property"""
        query = update.callback_query
        property_id = int(query.data.split('_')[1])
        
        prop = self.db.get_property(property_id)
        
        if prop:
            user_id = update.effective_user.id
            is_owner = (prop.user_id == user_id)
            
            await query.edit_message_text(
                prop.to_text(),
                reply_markup=self._get_property_actions_keyboard(property_id, is_owner)
            )
        else:
            await query.edit_message_text("❌ Property not found.")
    
    async def delete_property(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Request confirmation before deleting a property"""
        query = update.callback_query
        property_id = int(query.data.split('_')[1])
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Yes, Delete", callback_data=f'confirm_delete_{property_id}'),
                InlineKeyboardButton("❌ No, Cancel", callback_data=f'view_{property_id}')
            ]
        ]
        
        await query.edit_message_text(
            "⚠️ Are you sure you want to delete this property?\n\n"
            "This action cannot be undone.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def confirm_delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Confirm and execute property deletion"""
        query = update.callback_query
        property_id = int(query.data.split('_')[2])
        user_id = update.effective_user.id
        
        if self.db.delete_property(property_id, user_id):
            await query.edit_message_text("✅ Property successfully deleted.")
        else:
            await query.edit_message_text("❌ Error deleting property.")


def main():
    """
    Main function to run the bot
    Sets up all handlers and starts polling for messages
    """
    
    # Check configuration
    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("Telegram bot token not configured!")
        print("❌ Please configure the .env file based on .env.example")
        return
    
    if not config.OPENAI_API_KEY:
        logger.error("OpenAI API key not configured!")
        print("❌ Please configure the .env file based on .env.example")
        return
    
    # Create bot instance
    bot = RealEstateBot()
    
    # Build application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler('start', bot.start))
    application.add_handler(CommandHandler('help', bot.help_command))
    application.add_handler(CommandHandler('cancel', bot.cancel))
    
    # Add callback query handler (for inline keyboard buttons)
    application.add_handler(CallbackQueryHandler(bot.handle_callback_query))
    
    # Add message handlers (text and voice)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        bot.handle_text_message
    ))
    
    application.add_handler(MessageHandler(
        filters.VOICE,
        bot.handle_voice_message
    ))
    
    # Start the bot
    logger.info("🤖 Real Estate Bot is starting...")
    print("✅ Bot successfully launched!")
    print("🔗 Press Ctrl+C to stop.")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
