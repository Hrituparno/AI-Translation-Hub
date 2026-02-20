# Deployment Checklist

## Choose Your Plan

### Option A: High Quality ($7/month)
- ✅ Best translation quality (Google Translate-like)
- ✅ NLLB-200 model
- ✅ Render Starter plan (2 GB RAM)
- ✅ Recommended for production

### Option B: Free ($0/month)
- ✅ Good translation quality
- ✅ MarianMT model
- ✅ Render Free plan (512 MB RAM)
- ✅ Good for testing/demos

---

## Deployment Steps

### 1. Prepare Your Code

**For High Quality (Option A):**
```bash
python toggle_model.py nllb
```

**For Free (Option B):**
```bash
python toggle_model.py marian
```

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 3. Deploy API to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Name**: `india-translate-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Starter ($7) or Free ($0)
5. Add environment variables:
   - **For High Quality**: `USE_NLLB_MODEL=true`, `ENABLE_QUANTIZATION=true`
   - **For Free**: `USE_NLLB_MODEL=false`, `ENABLE_QUANTIZATION=false`
6. Click "Create Web Service"
7. Wait 5-10 minutes
8. **Copy your API URL**: `https://india-translate-api.onrender.com`

### 4. Update Streamlit UI

Edit `ui/app.py` and update the API URL:
```python
API_URL = os.getenv("API_URL", "https://YOUR-API-URL.onrender.com")
```

Push changes:
```bash
git add ui/app.py
git commit -m "Update API URL"
git push
```

### 5. Deploy UI to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `streamlit_app.py`
6. Add environment variable: `API_URL=https://your-api.onrender.com`
7. Click "Deploy!"
8. Wait 2-3 minutes
9. **Your app is live!** 🎉

---

## Testing

### Test API
```bash
curl https://your-api.onrender.com/health
```

### Test Translation
Visit your Streamlit app and try:
- Input: "Hello, how are you?"
- From: English
- To: Hindi
- Expected: "नमस्ते, आप कैसे हैं?"

---

## Checklist

- [ ] Choose plan (High Quality or Free)
- [ ] Run toggle_model.py
- [ ] Push code to GitHub
- [ ] Deploy API to Render
- [ ] Copy API URL
- [ ] Update ui/app.py with API URL
- [ ] Push updated code
- [ ] Deploy UI to Streamlit Cloud
- [ ] Test API health endpoint
- [ ] Test translation in UI
- [ ] Share your app! 🚀

---

## Your URLs

After deployment, save these:

- **API**: https://_________________.onrender.com
- **UI**: https://_________________.streamlit.app
- **API Docs**: https://_________________.onrender.com/docs

---

## Need Help?

See `DEPLOYMENT_GUIDE.md` for detailed instructions.
