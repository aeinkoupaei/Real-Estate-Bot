"""
AI Handler for Real Estate Bot (OpenAI GPT-based)
"""
import json
import re
import logging

import openai

import config


class GptHandler:
    """
    Handles property information extraction using OpenAI GPT models.
    Name retained for compatibility with existing imports.
    """

    def __init__(self):
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing from environment variables.")

        openai.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL
        openai.api_base = ""

    def extract_property_info(self, user_text):
        try:
            prompt = f"{config.PROPERTY_EXTRACTION_PROMPT}\n\nUser's text:\n{user_text}"
            result_text = self._chat(prompt).strip()

            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                property_data = json.loads(json_match.group(0))
                return self._clean_property_data(property_data)
            return None
        except Exception as exc:
            logging.error("Error extracting property information: %s", exc)
            return None

    def extract_search_filters(self, user_text):
        try:
            prompt = f"{config.SEARCH_QUERY_PROMPT}\n\nUser's request:\n{user_text}"
            result_text = self._chat(prompt).strip()

            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                filters = json.loads(json_match.group(0))
                return self._clean_filters(filters)
            return {}
        except Exception as exc:
            logging.error("Error extracting search filters: %s", exc)
            return {}

    def generate_response(self, prompt, context=None):
        try:
            if context:
                full_prompt = f"{context}\n\n{prompt}"
            else:
                full_prompt = prompt

            return self._chat(full_prompt).strip()
        except Exception as exc:
            logging.error("Error generating response: %s", exc)
            return "I couldn't generate an appropriate response."

    def validate_property_data(self, property_data):
        required_fields = ['title', 'property_type', 'city', 'area', 'price']
        missing_fields = [field for field in required_fields if not property_data.get(field)]
        is_valid = len(missing_fields) == 0
        return is_valid, missing_fields, property_data

    def ask_for_missing_info(self, missing_fields):
        field_names = {
            'title': 'Property title',
            'property_type': 'Property type (apartment, house, villa, etc.)',
            'city': 'City',
            'neighborhood': 'Neighborhood',
            'address': 'Address',
            'area': 'Size/Area',
            'price': 'Price',
            'rooms': 'Number of bedrooms',
            'floor': 'Floor number',
            'year_built': 'Year built'
        }
        
        missing_names = [field_names.get(f, f) for f in missing_fields]

        message = "⚠️ The following information is missing:\n\n"
        for name in missing_names:
            message += f"• {name}\n"

        message += "\nPlease provide the complete information."
        return message

    def summarize_properties(self, properties):
        if not properties:
            return "Unfortunately, no properties were found matching your criteria."

        count = len(properties)
        if count == 1:
            return "Found 1 property matching your search."
        return f"Found {count} properties matching your search."

    def _clean_property_data(self, data):
        cleaned = {}
        for key, value in data.items():
            if value is None or value == 'null' or value == '':
                continue

            if key in ['area', 'price']:
                try:
                    cleaned[key] = float(value)
                except (ValueError, TypeError):
                    continue
            elif key in ['rooms', 'floor', 'year_built']:
                try:
                    cleaned[key] = int(value)
                except (ValueError, TypeError):
                    continue
            elif key in ['parking', 'elevator', 'storage']:
                if isinstance(value, bool):
                    cleaned[key] = value
                elif isinstance(value, str):
                    cleaned[key] = value.lower() in ['true', 'yes', '1', 'has', 'available']
            else:
                cleaned[key] = str(value).strip()

        return cleaned

    def _clean_filters(self, filters):
        cleaned = {}
        for key, value in filters.items():
            if value is None or value == 'null' or value == '':
                continue

            if key in ['min_area', 'max_area', 'min_price', 'max_price']:
                try:
                    cleaned[key] = float(value)
                except (ValueError, TypeError):
                    continue
            elif key == 'rooms':
                try:
                    cleaned[key] = int(value)
                except (ValueError, TypeError):
                    continue
            elif key in ['parking', 'elevator']:
                if isinstance(value, bool):
                    cleaned[key] = value
                elif isinstance(value, str):
                    cleaned[key] = value.lower() in ['true', 'yes', '1', 'required', 'needed']
            else:
                cleaned[key] = str(value).strip()

        return cleaned

    def chat_response(self, user_message, conversation_context=""):
        system_prompt = """
You are an intelligent real estate assistant that responds in English.
Your job is to help users manage property information.
Your responses should be polite, helpful, and in simple language.
"""

        full_prompt = f"{system_prompt}\n\n"

        if conversation_context:
            full_prompt += f"Conversation context:\n{conversation_context}\n\n"

        full_prompt += f"User's message:\n{user_message}\n\nResponse:"

        return self.generate_response(full_prompt)

    def _chat(self, prompt):
        """
        Helper to call OpenAI ChatCompletion API.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return response["choices"][0]["message"]["content"]
        except Exception as exc:
            logging.error("Error calling OpenAI API: %s", exc)
            raise
