# Deployment Guide for Streamlit Cloud

## Prerequisites
- GitHub account
- Code pushed to a GitHub repository
- Streamlit Cloud account (free at share.streamlit.io)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your repository has these files:
- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Excludes sensitive files
- ✅ `README.md` - Documentation
- ✅ `runtime.txt` - Python version (optional)

### 2. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Patrol Shapefile Downloader"

# Create main branch
git branch -M main

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/streamlit_patrol.git

# Push
git push -u origin main
```

### 3. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Click "Sign in with GitHub"
   - Authorize Streamlit Cloud

2. **Create New App**
   - Click "New app" button
   - Fill in the form:
     - **Repository**: Select `yourusername/streamlit_patrol`
     - **Branch**: `main`
     - **Main file path**: `app.py`
     - **App URL** (optional): Choose custom URL

3. **Advanced Settings** (Optional)
   - Click "Advanced settings"
   - Set Python version: `3.11`
   - Add secrets if needed (see below)

4. **Deploy**
   - Click "Deploy!"
   - Wait 2-5 minutes for deployment
   - Your app will be live at: `https://[your-app-name].streamlit.app`

### 4. Configure Secrets (Optional)

If you want to pre-configure the EarthRanger server URL:

1. In Streamlit Cloud, go to your app
2. Click "⋮" (three dots) → "Settings"
3. Go to "Secrets" section
4. Add:
```toml
[earthranger]
server = "https://your-server.pamdas.org"
```
5. Click "Save"
6. Update `app.py` to use secrets (see QUICKSTART.md)

### 5. Update Your App

After making changes to your code:

```bash
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will automatically redeploy your app!

## Monitoring and Management

### View Logs
- In Streamlit Cloud, go to your app
- Click "Manage app" → "Logs"
- View real-time logs and errors

### Reboot App
- Click "⋮" → "Reboot app"
- Use if app becomes unresponsive

### Update Settings
- Click "⋮" → "Settings"
- Change Python version, secrets, etc.

### Delete App
- Click "⋮" → "Settings" → "Delete app"

## Troubleshooting

### Deployment Fails

**Error: "Requirements installation failed"**
- Check `requirements.txt` syntax
- Ensure package names are correct
- Check Python version compatibility

**Error: "ModuleNotFoundError"**
- Add missing package to `requirements.txt`
- Push changes to trigger redeployment

### App Crashes

**Check logs** in Streamlit Cloud:
1. Go to your app dashboard
2. Click "Manage app"
3. View "Logs" tab
4. Look for error messages

**Common issues:**
- Memory limit exceeded (reduce data processing)
- Timeout (optimize slow operations)
- Missing dependencies (update requirements.txt)

## Resource Limits (Free Tier)

Streamlit Cloud free tier includes:
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Unlimited apps
- ✅ Unlimited viewers

For larger deployments, consider:
- Streamlit Cloud Teams/Enterprise
- Self-hosting on cloud platforms (AWS, Azure, GCP)

## Custom Domain (Teams/Enterprise)

For custom domains:
1. Upgrade to Teams or Enterprise
2. Follow custom domain setup in Streamlit docs
3. Configure DNS settings

## Security Best Practices

### DO:
- ✅ Use secrets for sensitive configuration
- ✅ Have users enter credentials in the app UI
- ✅ Keep `.gitignore` updated
- ✅ Use HTTPS (automatic with Streamlit Cloud)
- ✅ Validate user inputs

### DON'T:
- ❌ Commit passwords or API keys
- ❌ Store credentials in code
- ❌ Share app URL publicly if it contains sensitive data
- ❌ Hardcode sensitive information

## Alternative Deployment Options

### Heroku
```bash
# Requires Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### AWS EC2 / Azure VM / GCP Compute
```bash
# On your VM:
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
nohup streamlit run app.py &
```

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Community Forum**: https://discuss.streamlit.io
- **GitHub Issues**: Open an issue in your repository

---

Good luck with your deployment! 🚀
