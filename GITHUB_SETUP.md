# GitHub Setup Guide

## Quick Method (Recommended)

Just run this script and follow the prompts:

```cmd
push_to_github.bat
```

It will:
1. Configure git with your info
2. Commit all files
3. Guide you to create GitHub repo
4. Push everything to GitHub

---

## Manual Method

If you prefer to do it manually:

### Step 1: Configure Git

```cmd
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 2: Commit Files

```cmd
git add .
git commit -m "Initial commit: Production-grade AI translation system"
```

### Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `AI-Translation-Hub`
3. Description: `Production-grade multilingual AI translation system for Indian languages`
4. Make it **Public**
5. **DO NOT** check "Initialize with README" (we already have one)
6. Click "Create repository"

### Step 4: Push to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```cmd
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AI-Translation-Hub.git
git push -u origin main
```

---

## Verify

After pushing, visit your repository:
```
https://github.com/YOUR_USERNAME/AI-Translation-Hub
```

You should see:
- ✅ All your code files
- ✅ README.md displayed on the homepage
- ✅ Documentation files
- ✅ Deployment configs

---

## Next Steps

After pushing to GitHub:

1. **Deploy API to Render**
   - See: `DEPLOYMENT_GUIDE.md`
   - Or: `SIMPLE_DEPLOY.md` for quick start

2. **Deploy UI to Streamlit Cloud**
   - See: `DEPLOY_CHECKLIST.md`

---

## Troubleshooting

### "Permission denied (publickey)"

You need to set up SSH keys or use HTTPS with personal access token.

**Quick fix**: Use HTTPS with token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select "repo" scope
4. Copy the token
5. Use this URL format:
   ```
   https://YOUR_TOKEN@github.com/YOUR_USERNAME/AI-Translation-Hub.git
   ```

### "Repository already exists"

If you already created the repo:
```cmd
git remote add origin https://github.com/YOUR_USERNAME/AI-Translation-Hub.git
git push -u origin main
```

### "Updates were rejected"

If the remote has changes:
```cmd
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## What Gets Pushed

✅ All source code
✅ Documentation
✅ Deployment configs
✅ Requirements
✅ Examples and tests

❌ Virtual environment (venv/)
❌ Cache files
❌ Model files
❌ Logs

---

## Repository Structure on GitHub

```
AI-Translation-Hub/
├── README.md                    # Main documentation
├── QUICKSTART.md               # Quick setup guide
├── DEPLOYMENT_GUIDE.md         # Deployment instructions
├── TRANSLATION_QUALITY_GUIDE.md # Quality guide
├── core/                       # Translation engine
├── api/                        # FastAPI backend
├── ui/                         # Streamlit frontend
├── requirements.txt            # Dependencies
├── render.yaml                 # Render config (high quality)
├── render-free.yaml           # Render config (free tier)
└── streamlit_app.py           # Streamlit entry point
```

---

## Making Updates

After initial push, to update:

```cmd
git add .
git commit -m "Description of changes"
git push
```

Both Render and Streamlit will auto-deploy on push! 🚀
