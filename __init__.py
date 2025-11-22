"""
Real Estate Bot - Telegram Real Estate Assistant

This package exposes the main modules required to run the Telegram-based
real estate assistant powered by OpenAI GPT-4o.
"""

__version__ = "1.0.0"
__author__ = "Aein Koupaei"
__description__ = (
    "Intelligent Telegram bot for managing real estate information using OpenAI GPT-4o."
)

# Re-export core classes for convenient imports
from .database import DatabaseManager, Property
from .gpt_handler import GptHandler
from .bot import RealEstateBot

__all__ = [
    'DatabaseManager',
    'Property',
    'GptHandler',
    'RealEstateBot',
]

