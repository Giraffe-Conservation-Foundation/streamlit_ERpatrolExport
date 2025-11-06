# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd streamlit_patrol

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the App

```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

### Step 3: Use the App

1. **Login** (sidebar):
   - Enter your EarthRanger server URL
   - Enter username and password
   - Click "Login"

2. **Download Patrols**:
   - Select patrol type
   - Choose date range
   - Click "Download Patrol Tracks"
   - Download the shapefile ZIP

## 📦 Deploy to Streamlit Cloud

### One-Time Setup:

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select:
     - Repository: `your-username/streamlit_patrol`
     - Branch: `main`
     - Main file path: `app.py`
   - Click "Deploy"

3. **Wait**: Deployment takes 2-5 minutes

4. **Share**: Get your public URL (e.g., `https://your-app.streamlit.app`)

## 🔧 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"  # Your color
backgroundColor = "#ffffff"
```

### Pre-configure Server URL

Create `.streamlit/secrets.toml`:
```toml
[earthranger]
server = "https://your-server.pamdas.org"
```

Then update `app.py` to read from secrets:
```python
import streamlit as st
default_server = st.secrets.get("earthranger", {}).get("server", "")
server = st.text_input("Server URL", value=default_server)
```

## ❓ Common Issues

### "Module not found: ecoscope"
```bash
pip install ecoscope-earth
```

### "No patrols found"
- Check your date range
- Verify patrol type is correct
- Ensure you have patrols in that time period

### Authentication fails
- Verify server URL includes `https://`
- Check username/password
- Ensure API access is enabled for your account

## 📞 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Contact your EarthRanger administrator

---

Happy tracking! 🗺️
