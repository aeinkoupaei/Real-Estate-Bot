#!/bin/bash

# Server Setup Script for Real Estate Bot
# Run this on your fresh Ubuntu/Debian server after SSH connection
# Usage: bash deploy_server_setup.sh

echo "=========================================="
echo "Real Estate Bot - Server Setup"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Please run as root: sudo bash deploy_server_setup.sh"
    exit 1
fi

echo "🔧 Step 1: Updating system..."
apt update && apt upgrade -y

echo ""
echo "🔧 Step 2: Installing Python and dependencies..."
apt install python3 python3-pip python3-venv git nano -y

echo ""
echo "🔧 Step 3: Installing the bot..."
read -p "Enter your GitHub repository URL (or press Enter to skip): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "Skipping git clone. Please upload your files manually."
    mkdir -p /root/Real-Estate-Bot
else
    cd /root
    git clone "$REPO_URL" Real-Estate-Bot
fi

cd /root/Real-Estate-Bot

echo ""
echo "🔧 Step 4: Creating virtual environment..."
python3 -m venv realassist
source realassist/bin/activate

echo ""
echo "🔧 Step 5: Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🔧 Step 6: Setting up environment variables..."
echo "Please enter your configuration:"
echo ""

read -p "Telegram Bot Token: " BOT_TOKEN
read -p "OpenAI API Key: " OPENAI_KEY

cat > .env << EOF
TELEGRAM_BOT_TOKEN=$BOT_TOKEN
OPENAI_API_KEY=$OPENAI_KEY
OPENAI_MODEL=gpt-4o
OPENAI_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe
DATABASE_URL=sqlite:///real_estate.db
LOG_LEVEL=INFO
EOF

chmod 600 .env
echo "✅ .env file created and secured"

echo ""
echo "🔧 Step 7: Testing the bot..."
echo "Starting bot for 10 seconds to test..."
timeout 10 python bot.py &
sleep 10
echo "Test complete!"

echo ""
echo "🔧 Step 8: Creating systemd service..."
cat > /etc/systemd/system/realestatebot.service << EOF
[Unit]
Description=Real Estate Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/Real-Estate-Bot
Environment="PATH=/root/Real-Estate-Bot/realassist/bin"
ExecStart=/root/Real-Estate-Bot/realassist/bin/python /root/Real-Estate-Bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "🔧 Step 9: Starting the bot service..."
systemctl daemon-reload
systemctl enable realestatebot
systemctl start realestatebot

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Your bot is now running 24/7!"
echo ""
echo "📋 Useful Commands:"
echo "  Check status:  systemctl status realestatebot"
echo "  View logs:     journalctl -u realestatebot -f"
echo "  Restart:       systemctl restart realestatebot"
echo "  Stop:          systemctl stop realestatebot"
echo ""
echo "🔍 Check bot status now:"
systemctl status realestatebot --no-pager
echo ""
echo "🎉 Your bot should now be running!"
echo "Send /start to your bot on Telegram to test."
echo ""

