# 🚀 Deployment Guide - Coaching Management System

This guide covers deploying the Coaching Management System to different platforms.

## 📋 Table of Contents
1. [Local Machine Setup](#local-machine-setup)
2. [Streamlit Cloud (Recommended)](#streamlit-cloud)
3. [Self-Hosted Server](#self-hosted-server)
4. [Docker Deployment](#docker-deployment)
5. [Google Sheets Integration](#google-sheets-integration)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ Local Machine Setup

### Quick Start (Windows, Mac, Linux)

```bash
# 1. Clone/download the project
cd coaching-management-system

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate sample data (optional)
python generate_sample_data.py

# 6. Run the app
streamlit run app.py

# App will open at http://localhost:8501
```

### Default Credentials
- **Password:** `admin123`
- **Change in:** `app.py` line 86

---

## ☁️ Streamlit Cloud Deployment (Recommended)

### Step 1: Prepare Repository

```bash
# Initialize git (if not done)
git init

# Create .gitignore to exclude sensitive files
echo "*.xlsx" > .gitignore
echo "coaching_data.xlsx" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "venv/" >> .gitignore

# Commit files
git add .
git commit -m "Initial commit: Coaching Management System"

# Push to GitHub
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Create GitHub Account** (if you don't have one)
   - Go to github.com
   - Sign up for free

2. **Push Code to GitHub**
   - Create new repository
   - Push your code there

3. **Deploy on Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Click "New app"
   - Select your GitHub repo and main file (app.py)
   - Click "Deploy"

4. **Configuration**
   - App will be assigned a URL: `https://yourname-coachingsystem.streamlit.app`
   - Share this URL with team

### Step 3: Configure Data Persistence

For storing data in Streamlit Cloud, use Streamlit Secrets:

1. Go to app settings
2. Create file `.streamlit/secrets.toml`:
   ```toml
   [connections.gsheets]
   spreadsheet = "your-spreadsheet-id"
   type = "service_account"
   ```

3. Create Google Service Account (see [Google Sheets Integration](#google-sheets-integration))

### Benefits
✅ Free hosting
✅ Automatic HTTPS
✅ Auto-deployed on push
✅ Built-in authentication options
✅ Easy to share

### Limitations
⚠️ Excel files don't persist between sessions (use Google Sheets instead)
⚠️ Free tier has monthly hour limits
⚠️ Public by default (add Streamlit authentication)

---

## 🖧 Self-Hosted Server

### Option 1: Linux Server (Ubuntu/Debian)

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install Python
sudo apt-get update
sudo apt-get install python3.9 python3-pip python3-venv

# 3. Clone repository
git clone https://github.com/yourname/coaching-system.git
cd coaching-system

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
pip install gunicorn

# 6. Create systemd service file
sudo nano /etc/systemd/system/coaching-app.service
```

Add this content:
```ini
[Unit]
Description=Coaching Management System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/user/coaching-system
Environment="PATH=/home/user/coaching-system/venv/bin"
ExecStart=/home/user/coaching-system/venv/bin/streamlit run app.py --server.port=8501

[Install]
WantedBy=multi-user.target
```

```bash
# 7. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable coaching-app
sudo systemctl start coaching-app
sudo systemctl status coaching-app

# 8. Access via: http://your-server-ip:8501
```

### Option 2: Windows Server

```batch
REM 1. Install Python 3.9+

REM 2. Create folder and navigate
mkdir C:\coaching-system
cd C:\coaching-system

REM 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

REM 4. Install dependencies
pip install -r requirements.txt

REM 5. Create batch file for startup
echo @echo off > start_app.bat
echo cd C:\coaching-system >> start_app.bat
echo venv\Scripts\activate >> start_app.bat
echo streamlit run app.py --server.port=8501 >> start_app.bat

REM 6. Add to Task Scheduler
REM - Windows Key → Task Scheduler
REM - Create Basic Task
REM - Set trigger: At startup
REM - Set action: Run start_app.bat
```

### Option 3: Using Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/coaching-system

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/coaching-system /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  coaching-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./coaching_data.xlsx:/app/coaching_data.xlsx
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
    restart: unless-stopped
```

### Deploy with Docker

```bash
# Build image
docker build -t coaching-system .

# Run container
docker run -d -p 8501:8501 -v $(pwd)/coaching_data.xlsx:/app/coaching_data.xlsx coaching-system

# Or use docker-compose
docker-compose up -d

# View logs
docker logs coaching-system

# Stop container
docker stop coaching-system
```

---

## 📊 Google Sheets Integration

### Step 1: Create Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Google Sheets API
4. Create Service Account:
   - Go to Credentials
   - Create Service Account
   - Create JSON key
   - Download and save as `credentials.json`

### Step 2: Modify app.py

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

def read_sheet_gsheets(sheet_name):
    sheet = client.open("Coaching Data").worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def write_sheet_gsheets(df, sheet_name):
    sheet = client.open("Coaching Data").worksheet(sheet_name)
    sheet.clear()
    sheet.append_table(df.values.tolist(), tab_index=0)
```

### Step 3: Share Google Sheet

1. Create Google Sheet named "Coaching Data"
2. Create sheets: Batches, Students, Payments
3. Share with service account email
4. Deploy with `credentials.json`

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Change default password in `config.py`
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (use nginx with SSL)
- [ ] Set up firewall rules
- [ ] Regular data backups
- [ ] Monitor access logs
- [ ] Update dependencies regularly
- [ ] Disable debug mode in production
- [ ] Use strong, complex passwords
- [ ] Implement user roles (future feature)

---

## 📝 Environment Variables

Create `.env` file:

```env
COACHING_APP_PASSWORD=your_secret_password_here
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
DATABASE_TYPE=excel
DEBUG_MODE=False
```

Load in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()
PASSWORD = os.getenv('COACHING_APP_PASSWORD', 'admin123')
```

---

## 🔄 Backup Strategy

### Daily Backups

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/coaching-system"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

cp coaching_data.xlsx "$BACKUP_DIR/coaching_data_$TIMESTAMP.xlsx"

# Keep only last 30 days
find $BACKUP_DIR -name "*.xlsx" -mtime +30 -delete
```

Schedule with cron:

```bash
# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## 📊 Monitoring & Logs

### Streamlit Logs

```bash
tail -f ~/.streamlit/logs/2024*.log
```

### Application Health Check

```python
# health_check.py
import requests

try:
    response = requests.get('http://localhost:8501')
    if response.status_code == 200:
        print("✅ App is running")
    else:
        print("❌ App returned error")
except:
    print("❌ App is offline")
```

---

## 🐛 Troubleshooting Deployment

### Issue: "Module not found" error
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Port already in use
```bash
# Solution: Change port in streamlit run command
streamlit run app.py --server.port=8502
```

### Issue: Excel file locked
```bash
# Solution: Use Google Sheets or implement file locking
# Or restart the app to release file handle
```

### Issue: Slow performance
```bash
# Solution: 
# 1. Archive old data (>1 year)
# 2. Use database instead of Excel for large datasets
# 3. Implement caching in Streamlit
```

---

## 📞 Support

For issues:
1. Check logs: `.streamlit/logs/`
2. Run locally first to isolate issues
3. Test with sample data
4. Check permissions and file access

---

**Happy Deploying! 🎉**
