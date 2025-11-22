# Real Estate Chatbot - Deployment Guide

How to deploy your chatbot for 24/7 operation so it's always accessible.

---

## Deployment Options Overview

| Option | Cost | Difficulty | Best For |
|--------|------|-----------|----------|
| **DigitalOcean** | $6/month | Easy | Recommended for beginners |
| **AWS EC2** | Free tier / $3+/month | Medium | Production with scaling |
| **Google Cloud** | Free tier / $5+/month | Medium | Integration with other Google services |
| **Heroku** | Free tier / $7+/month | Very Easy | Quick deployment |
| **Railway** | Free tier / $5+/month | Very Easy | Modern, simple |
| **PythonAnywhere** | Free tier / $5+/month | Easy | Python-specific hosting |
| **Your own VPS** | Varies | Medium | Full control |

**Recommended for this project**: DigitalOcean, Railway, or PythonAnywhere

---

## Option 1: DigitalOcean Droplet (Recommended)

### Why DigitalOcean?
- Simple setup
- $6/month basic plan is perfect for this bot
- Excellent documentation
- Reliable uptime
- Easy to scale

### Step-by-Step Setup

#### 1. Create DigitalOcean Account
1. Go to https://www.digitalocean.com/
2. Sign up (you may get free credits)
3. Verify your account

#### 2. Create a Droplet
1. Click **Create** → **Droplets**
2. Choose:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic
   - **CPU options**: Regular - $6/month (1GB RAM)
   - **Datacenter**: Choose closest to your users
   - **Authentication**: SSH keys (recommended) or password
3. Click **Create Droplet**
4. Wait 1-2 minutes for creation

#### 3. Connect to Your Droplet
```bash
# Replace YOUR_DROPLET_IP with your actual IP
ssh root@YOUR_DROPLET_IP
```

#### 4. Setup Python Environment
```bash
# Update system
apt update && apt upgrade -y

# Install Python and pip
apt install python3 python3-pip python3-venv git -y

# Verify installation
python3 --version
pip3 --version
```

#### 5. Upload Your Bot
**Option A: Using Git (Recommended)**
```bash
# If your code is on GitHub
git clone https://github.com/aeinkoupaei/Real-Estate-Bot.git
cd Real-Estate-Bot
```

**Option B: Using SCP (from your local machine)**
```bash
# Run this on your LOCAL machine, not the server
cd /Users/aeinkoupaei/Desktop/Projects
scp -r Real-Estate-Bot root@YOUR_DROPLET_IP:/root/
```

#### 6. Setup Bot on Server
```bash
# Navigate to bot directory
cd /root/Real-Estate-Bot

# Create virtual environment
python3 -m venv realassist

# Activate virtual environment
source realassist/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 7. Configure Environment Variables
```bash
# Create .env file
nano .env
```

Add your configuration:
```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=models/gemini-2.5-flash
DATABASE_URL=sqlite:///real_estate.db
LOG_LEVEL=INFO
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

#### 8. Test the Bot
```bash
# Test run
python3 bot.py
```

If it works, press `Ctrl+C` to stop.

#### 9. Setup Systemd Service (Auto-start & Auto-restart)

Create a systemd service file:
```bash
nano /etc/systemd/system/realestatebot.service
```

Add this content:
```ini
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
```

Save and exit (`Ctrl+X`, `Y`, `Enter`).

#### 10. Start and Enable the Service
```bash
# Reload systemd
systemctl daemon-reload

# Start the bot
systemctl start realestatebot

# Enable auto-start on boot
systemctl enable realestatebot

# Check status
systemctl status realestatebot
```

You should see "active (running)" in green!

#### 11. Useful Commands
```bash
# Check if bot is running
systemctl status realestatebot

# View live logs
journalctl -u realestatebot -f

# Restart bot
systemctl restart realestatebot

# Stop bot
systemctl stop realestatebot

# View recent logs
journalctl -u realestatebot -n 100
```

### Done! Your bot is now running 24/7!

---

## Option 2: Railway (Easiest, Modern)

### Why Railway?
- Extremely easy deployment
- Free tier available
- GitHub integration
- Automatic deployments
- Built-in monitoring

### Step-by-Step

#### 1. Prepare Your Code

Create `Procfile` in your project root:
```bash
cd /Users/aeinkoupaei/Desktop/Projects/Real-Estate-Bot
nano Procfile
```

Add:
```
bot: python bot.py
```

Create `railway.json` (optional, for configuration):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python bot.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. Push to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Prepare for Railway deployment"

# Create a repo on GitHub, then:
git remote add origin https://github.com/aeinkoupaei/Real-Estate-Bot.git
git branch -M main
git push -u origin main
```

#### 3. Deploy on Railway
1. Go to https://railway.app/
2. Sign up with GitHub
3. Click **New Project**
4. Select **Deploy from GitHub repo**
5. Choose your repository
6. Railway will auto-detect Python and deploy

#### 4. Set Environment Variables
1. In Railway dashboard, click your project
2. Go to **Variables** tab
3. Add:
   - `TELEGRAM_BOT_TOKEN`
   - `GEMINI_API_KEY`
   - `GEMINI_MODEL`
   - `DATABASE_URL`
   - `LOG_LEVEL`

#### 5. Deploy
Railway will automatically deploy and restart your bot!

**View logs**: Click **Deployments** → Select latest → **View Logs**

### Done! Railway handles 24/7 operation automatically!

---

## Option 3: PythonAnywhere (Python-Specific)

### Why PythonAnywhere?
- Python-focused hosting
- Free tier available
- Simple web interface
- Good for beginners

### Step-by-Step

#### 1. Create Account
1. Go to https://www.pythonanywhere.com/
2. Sign up for a free account

#### 2. Upload Your Code
1. Click **Files** tab
2. Upload your project files, or use Git:

```bash
# In PythonAnywhere console
git clone https://github.com/aeinkoupaei/Real-Estate-Bot.git
cd Real-Estate-Bot
```

#### 3. Setup Virtual Environment
```bash
# In PythonAnywhere Bash console
cd Real-Estate-Bot
python3 -m venv realassist
source realassist/bin/activate
pip install -r requirements.txt
```

#### 4. Create .env File
Create `.env` with your API keys (use the Files interface or nano).

#### 5. Setup Always-On Task
1. Go to **Tasks** tab
2. Create a new task:
   - Command: `/home/aeinkoupaei/Real-Estate-Bot/realassist/bin/python /home/aeinkoupaei/Real-Estate-Bot/bot.py`
   - Schedule: Daily at midnight (for auto-restart)

#### 6. Start Manually First
```bash
# In console
cd Real-Estate-Bot
source realassist/bin/activate
python bot.py
```

Keep this console tab open to keep bot running.

**Note**: Free tier requires you to log in every 3 months to keep bot active.

---

## Option 4: Docker Deployment (Advanced)

### Why Docker?
- Consistent environment
- Easy to deploy anywhere
- Portable
- Professional solution

### Setup

#### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run bot
CMD ["python", "bot.py"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: realestatebot
    restart: always
    env_file:
      - .env
    volumes:
      - ./real_estate.db:/app/real_estate.db
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### 3. Create .dockerignore
```
realassist/
__pycache__/
*.pyc
.env
.git
*.md
```

#### 4. Build and Run
```bash
# Build image
docker-compose build

# Start bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop bot
docker-compose down
```

#### 5. Deploy to any Docker host
- DigitalOcean App Platform
- AWS ECS
- Google Cloud Run
- Any VPS with Docker

---

## Option 5: Using Screen/Tmux (Simple VPS)

If you have a VPS but don't want systemd:

### Using Screen
```bash
# Install screen
apt install screen -y

# Start a new screen session
screen -S rebot

# Inside screen, start bot
cd Real-Estate-Bot
source realassist/bin/activate
python bot.py

# Detach from screen: Press Ctrl+A, then D

# Reattach later
screen -r rebot

# List sessions
screen -ls
```

### Using Tmux
```bash
# Install tmux
apt install tmux -y

# Start tmux session
tmux new -s rebot

# Inside tmux, start bot
cd Real-Estate-Bot
source realassist/bin/activate
python bot.py

# Detach: Press Ctrl+B, then D

# Reattach
tmux attach -t rebot
```

---

## Monitoring Your Bot

### Check if Bot is Running

**On systemd:**
```bash
systemctl status realestatebot
```

**On Docker:**
```bash
docker-compose ps
```

**Check Telegram:**
Send `/start` to your bot. If it responds, it's running!

### View Logs

**On systemd:**
```bash
# Live logs
journalctl -u realestatebot -f

# Last 100 lines
journalctl -u realestatebot -n 100

# Today's logs
journalctl -u realestatebot --since today
```

**On Docker:**
```bash
docker-compose logs -f
```

**On Railway:**
- Dashboard → Deployments → View Logs

### Setup Log Rotation

For systemd, logs are automatically rotated. For others:

```bash
nano /etc/logrotate.d/realestatebot
```

Add:
```
/var/log/realestatebot.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## Auto-Restart on Failure

### Systemd (Built-in)
Already configured with:
```ini
Restart=always
RestartSec=10
```

### Docker (Built-in)
```yaml
restart: always
```

### Manual Script
Create `monitor.sh`:
```bash
#!/bin/bash
while true; do
    if ! pgrep -f "python bot.py" > /dev/null; then
        echo "Bot crashed! Restarting..."
        cd /root/Real-Estate-Bot
        source realassist/bin/activate
        python bot.py &
    fi
    sleep 60
done
```

Make executable and run:
```bash
chmod +x monitor.sh
nohup ./monitor.sh &
```

---

## Performance & Scaling

### Current Setup Handles:
- Up to 100 concurrent users
- Thousands of properties
- Moderate voice processing

### If You Need More:
1. **Upgrade server** (more RAM/CPU)
2. **Use PostgreSQL** instead of SQLite
3. **Add Redis** for caching
4. **Load balancer** for multiple instances
5. **Use webhooks** instead of polling

---

## Security Best Practices

### 1. Firewall Setup
```bash
# On Ubuntu/Debian
ufw allow ssh
ufw allow 443
ufw enable
```

### 2. Secure Your .env
```bash
chmod 600 .env
```

### 3. Regular Updates
```bash
# System updates
apt update && apt upgrade -y

# Python packages
pip install --upgrade -r requirements.txt
```

### 4. Use SSH Keys (Not Passwords)
Generate on your local machine:
```bash
ssh-keygen -t ed25519
```

Add to server:
```bash
ssh-copy-id root@YOUR_SERVER_IP
```

### 5. Monitor Logs for Errors
```bash
journalctl -u realestatebot -p err
```

---

## Cost Comparison

| Provider | Free Tier | Paid Plan | Best For |
|----------|-----------|-----------|----------|
| DigitalOcean | No | $6/month | Production |
| Railway | 500 hrs/month | $5/month | Easy deployment |
| PythonAnywhere | Limited | $5/month | Beginners |
| Heroku | No (discontinued free tier) | $7/month | Quick deploy |
| AWS EC2 | 12 months | $3+/month | Enterprise |
| Google Cloud | $300 credit | $5+/month | Google integration |

---

## Recommended Setup by User Level

### Beginner
**Railway** or **PythonAnywhere**
- Easiest setup
- Web interface
- No server management

### Intermediate
**DigitalOcean Droplet**
- Full control
- Learn server management
- Best value

### Advanced
**Docker on AWS/GCP**
- Scalable
- Professional
- CI/CD integration

---

## 🐛 Troubleshooting

### Bot Not Responding
```bash
# Check if running
systemctl status realestatebot

# Check logs
journalctl -u realestatebot -n 50

# Restart
systemctl restart realestatebot
```

### Out of Memory
```bash
# Check memory
free -h

# If needed, add swap
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Database Locked
```bash
# Usually happens if SQLite is accessed by multiple processes
# Make sure only one bot instance is running
pkill -f "python bot.py"
systemctl start realestatebot
```

### Can't Connect to Server
```bash
# Check if SSH is running
systemctl status ssh

# Check firewall
ufw status

# Try password auth if SSH key fails
ssh -o PreferredAuthentications=password root@YOUR_IP
```

---

## Webhooks vs Polling

Current bot uses **polling** (asks Telegram for updates).

For production, consider **webhooks**:

### Benefits of Webhooks
- Faster response
- Lower server load
- More efficient

### Setup Webhooks
1. Need HTTPS domain
2. Modify bot.py:

```python
# Instead of:
application.run_polling()

# Use:
application.run_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path="your-bot-token",
    webhook_url=f"https://yourdomain.com:8443/{TOKEN}"
)
```

3. Setup nginx reverse proxy
4. Get SSL certificate (Let's Encrypt)

**For now, polling is fine!** Switch to webhooks when scaling.

---

## Deployment Checklist

Before deploying:
- [ ] Test bot locally
- [ ] Have Telegram Bot Token
- [ ] Have OpenAI API Key
- [ ] Choose hosting provider
- [ ] Prepare .env file
- [ ] Test component tests pass
- [ ] Backup database if migrating

After deploying:
- [ ] Bot responds to /start
- [ ] Voice messages work
- [ ] Can register property
- [ ] Can search properties
- [ ] Logs are accessible
- [ ] Auto-restart works (test by killing process)
- [ ] Setup monitoring

---

## Quick Start Recommendation

**For fastest 24/7 deployment:**

1. **Choose Railway** (easiest) or **DigitalOcean** (best value)
2. **Follow the guide above** for your choice
3. **Set environment variables**
4. **Deploy and test**
5. **Monitor logs** for first few hours
6. **Done!**

Your bot will now run 24/7 automatically!

---

## Need Help?

Common issues:
- **Bot stops randomly**: Check logs, ensure enough RAM
- **Can't connect**: Check firewall, SSH settings
- **Database errors**: Ensure only one instance running
- **Voice not working**: Verify OpenAI API key, check internet

---

**Your bot is ready for 24/7 operation!** Choose a deployment method and follow the guide above.

