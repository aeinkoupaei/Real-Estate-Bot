#!/bin/bash

# Real Estate Bot - Quick Start Script
# This script activates the virtual environment and starts the bot

echo "=========================================="
echo "Real Estate Management Chatbot"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your API keys."
    echo "See env.example for reference."
    echo ""
echo "Required variables:"
echo "  - TELEGRAM_BOT_TOKEN"
echo "  - OPENAI_API_KEY"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [ -d "realassist" ]; then
    source realassist/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found!"
    echo "Please create it first with: python3 -m venv realassist"
    exit 1
fi

# Check if dependencies are installed
echo ""
echo "📦 Checking dependencies..."
python -c "import telegram, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing"
    echo "Installing requirements..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ All dependencies present"
fi

# Run component tests
echo ""
echo "🧪 Running component tests..."
python test_bot_components.py
echo ""

# Ask user if they want to continue
read -p "Start the bot now? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Start the bot
echo ""
echo "🚀 Starting bot..."
echo "Press Ctrl+C to stop"
echo ""
python bot.py

