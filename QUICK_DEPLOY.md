# Quick Deployment Guide - 3 Easiest Options

Choose your deployment method and follow the steps!

---

## Option 1: Railway (Easiest - 5 minutes)

**Best for**: Beginners, quick deployment, automatic updates

### Steps:

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/aeinkoupaei/Real-Estate-Bot.git
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Wait for deployment (automatic)

3. **Add Environment Variables**
   - Click on your project → "Variables" tab
   - Add these variables:
     - `TELEGRAM_BOT_TOKEN` = your-bot-token
     - `OPENAI_API_KEY` = your-openai-key
     - `OPENAI_MODEL` = gpt-4o
     - `OPENAI_TRANSCRIPTION_MODEL` = gpt-4o-mini-transcribe
     - `LOG_LEVEL` = INFO

4. **Done!**
   - Bot deploys automatically
   - Check logs in Railway dashboard
   - Test by sending /start to your bot

**Cost**: Free tier (500 hours/month) or $5/month

---

## Option 2: DigitalOcean (Best Value - 15 minutes)

**Best for**: Production use, full control, learning

### Steps:

1. **Create Droplet**
   - Go to https://digitalocean.com
   - Create account (may get $200 credit)
   - Create Droplet:
     - Ubuntu 22.04 LTS
     - Basic plan - $6/month
     - Choose datacenter region
   - Wait 1-2 minutes

2. **Connect to Server**
   ```bash
   ssh root@YOUR_DROPLET_IP
   ```

3. **Upload and Run Setup Script**
   
   From your **local machine**:
   ```bash
   scp deploy_server_setup.sh root@YOUR_DROPLET_IP:/root/
   ```
   
   On the **server**:
   ```bash
   cd /root
   bash deploy_server_setup.sh
   ```
   
   The script will:
   - Install Python and dependencies
   - Setup your bot
   - Ask for API keys
   - Create systemd service
   - Start bot automatically

4. **Done!**
   - Bot runs 24/7
   - Auto-restarts on failure
   - Check status: `systemctl status realestatebot`

**Cost**: $6/month

---

## Option 3: Docker (Any Server - 10 minutes)

**Best for**: Professional deployment, portability

### Prerequisites:
- Any server with Docker installed
- SSH access to server

### Steps:

1. **Upload Code to Server**
   ```bash
   # From local machine
   scp -r /Users/aeinkoupaei/Desktop/Projects/Real-Estate-Bot root@YOUR_SERVER_IP:/root/
   ```

2. **Connect to Server**
   ```bash
   ssh root@YOUR_SERVER_IP
   ```

3. **Install Docker** (if not installed)
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

4. **Setup and Run**
   ```bash
   cd /root/Real-Estate-Bot
   
   # Create .env file
   nano .env
   # Add your TELEGRAM_BOT_TOKEN and OPENAI_API_KEY
   # Save: Ctrl+X, Y, Enter
   
   # Build and run
   docker-compose up -d
   
   # Check logs
   docker-compose logs -f
   ```

5. **Done!**
   - Bot runs in Docker container
   - Auto-restarts automatically
   - Check status: `docker-compose ps`

**Cost**: Depends on your server provider

---

## Quick Comparison

| Feature | Railway | DigitalOcean | Docker |
|---------|---------|--------------|--------|
| **Setup Time** | 5 min | 15 min | 10 min |
| **Difficulty** | Easy | Medium | Medium |
| **Cost** | Free/\$5 | \$6/month | Varies |
| **Best For** | Quick start | Production | Professional |
| **Auto-restart** | Yes | Yes | Yes |
| **Monitoring** | Built-in | Manual | Manual |
| **Scalability** | Easy | Medium | Easy |

---

## My Recommendation

### For Your First Deployment:
**→ Use Railway**
- Fastest setup
- Free to start
- Perfect for testing

### For Production:
**→ Use DigitalOcean**
- Best value
- Full control
- Learn server management

### For Professional Setup:
**→ Use Docker on any cloud**
- Portable
- Professional
- Works anywhere

---

## After Deployment Checklist

No matter which option you chose:

- [ ] Bot responds to `/start` command
- [ ] Voice messages work
- [ ] Can register a property
- [ ] Can search properties
- [ ] Can edit properties
- [ ] Bot stays running after you close terminal
- [ ] Bot restarts if it crashes (test by killing process)

**Test everything before considering it deployed!**

---

## Common Issues

### Bot Not Responding
**Railway**: Check Variables tab, ensure all API keys are set  
**DigitalOcean**: Run `systemctl status realestatebot`  
**Docker**: Run `docker-compose logs`

### "Connection Error"
- Check API keys are correct
- Verify internet connection on server
- Check Telegram bot token is valid

### "Module Not Found"
**Railway**: Will auto-install from requirements.txt  
**DigitalOcean**: Run `pip install -r requirements.txt`  
**Docker**: Rebuild with `docker-compose build`

### Bot Stops After Closing Terminal
**Railway**: Automatic, no issue  
**DigitalOcean**: Use systemd service (deploy_server_setup.sh does this)  
**Docker**: Use `-d` flag: `docker-compose up -d`

---

## Need Help?

1. **Check logs first**:
   - Railway: Dashboard → Logs
   - DigitalOcean: `journalctl -u realestatebot -f`
   - Docker: `docker-compose logs -f`

2. **Verify API keys**:
   - Test Telegram token: Send request to `https://api.telegram.org/bot<TOKEN>/getMe`
   - Test OpenAI key: Run a quick curl against `https://api.openai.com/v1/models`

3. **Test locally first**:
   ```bash
   python bot.py
   ```
   If it works locally but not on server, it's a deployment issue.

---

## Let's Deploy!

Choose your method above and follow the steps. Your bot will be running 24/7 in less than 15 minutes!

**After deployment, send /start to your bot on Telegram to verify it's working!**

Good luck!

