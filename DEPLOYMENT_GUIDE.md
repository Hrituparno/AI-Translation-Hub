# Deployment Guide - Render & Streamlit Cloud

## Quick Answer

### For Render (API Backend)

**Option 1: High Quality (Recommended) - $7/month**
- Plan: Starter (2 GB RAM)
- Uses NLLB model (Google Translate quality)
- File: `render.yaml`

**Option 2: Free Tier - $0/month**
- Plan: Free (512 MB RAM)
- Uses MarianMT model (lightweight)
- File: `render-free.yaml`

### For Streamlit Cloud (UI Frontend)

- **Free** (1 GB RAM)
- Uses your Render API backend
- File: `streamlit_app.py`

---

## Step-by-Step: Deploy to Render

### Option 1: High Quality ($7/month)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add translation system"
   git push origin main
   ```

2. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click "New +" → "Web Service"

3. **Connect Repository**
   - Connect your GitHub account
   - Select your repository

4. **Configure Service**
   - Name: `india-translate-api`
   - Environment: `Python 3`
   - Region: `Oregon (US West)`
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

5. **Select Plan**
   - Choose: **Starter ($7/month)** - 2 GB RAM

6. **Add Environment Variables**
   ```
   USE_NLLB_MODEL = true
   ENABLE_QUANTIZATION = true
   MAX_MODELS_IN_MEMORY = 1
   LOG_LEVEL = INFO
   ```

7. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Note your API URL: `https://india-translate-api.onrender.com`

### Option 2: Free Tier ($0/month)

Follow same steps but:

**Step 5: Select Plan**
- Choose: **Free** - 512 MB RAM

**Step 6: Environment Variables**
```
USE_NLLB_MODEL = false
ENABLE_QUANTIZATION = false
MAX_MODELS_IN_MEMORY = 2
LOG_LEVEL = INFO
```

**Before deploying**, update `core/config.py`:
```python
USE_NLLB_MODEL = False  # Use lightweight MarianMT
```

---

## Step-by-Step: Deploy to Streamlit Cloud

### Prerequisites
- Render API deployed and running
- GitHub repository with your code

### Steps

1. **Update UI to Use Render API**
   
   Edit `ui/app.py`, find the API URL line and update:
   ```python
   API_URL = os.getenv("API_URL", "https://india-translate-api.onrender.com")
   ```
   Replace with your actual Render URL.

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Configure for Streamlit Cloud"
   git push origin main
   ```

3. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

4. **Deploy New App**
   - Click "New app"
   - Repository: Select your repo
   - Branch: `main`
   - Main file path: `streamlit_app.py`

5. **Advanced Settings (Optional)**
   - Python version: `3.9`
   - Add environment variable:
     ```
     API_URL = https://your-render-api.onrender.com
     ```

6. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes
   - Your app will be at: `https://your-app.streamlit.app`

---

## Configuration Files

### For Render

**High Quality (Starter Plan):**
- Use: `render.yaml`
- Memory: 2 GB
- Model: NLLB
- Cost: $7/month

**Free Tier:**
- Use: `render-free.yaml`
- Memory: 512 MB
- Model: MarianMT
- Cost: $0/month

### For Streamlit Cloud

- Entry point: `streamlit_app.py`
- Config: `.streamlit/config.toml`
- Memory: 1 GB (free)

---

## Environment Variables

### Render API

| Variable | High Quality | Free Tier |
|----------|--------------|-----------|
| USE_NLLB_MODEL | true | false |
| ENABLE_QUANTIZATION | true | false |
| MAX_MODELS_IN_MEMORY | 1 | 2 |
| LOG_LEVEL | INFO | INFO |

### Streamlit Cloud

| Variable | Value |
|----------|-------|
| API_URL | Your Render API URL |

---

## Testing Deployment

### Test Render API

```bash
# Health check
curl https://your-api.onrender.com/health

# Test translation
curl -X POST https://your-api.onrender.com/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","source_lang":"en","target_lang":"hi"}'
```

### Test Streamlit UI

1. Visit your Streamlit URL
2. Try translating "Hello" from English to Hindi
3. Check if translation appears

---

## Troubleshooting

### Render Issues

**"Out of Memory" Error**
- Switch to Starter plan ($7/month)
- Or use `render-free.yaml` with MarianMT

**Slow First Request**
- Normal! Model downloads on first use (45-60s)
- Subsequent requests are fast (3-5s)

**Build Failed**
- Check Python version (3.9 recommended)
- Verify `requirements.txt` is correct

### Streamlit Issues

**"Cannot connect to API"**
- Check API_URL is correct
- Verify Render API is running
- Check Render API health: `/health`

**App Crashes**
- Check Streamlit logs
- Verify `streamlit_app.py` exists
- Check Python version compatibility

---

## Cost Breakdown

### Recommended Setup (High Quality)

| Service | Plan | Cost | Memory |
|---------|------|------|--------|
| Render API | Starter | $7/month | 2 GB |
| Streamlit UI | Free | $0/month | 1 GB |
| **Total** | | **$7/month** | |

### Budget Setup (Free)

| Service | Plan | Cost | Memory |
|---------|------|------|--------|
| Render API | Free | $0/month | 512 MB |
| Streamlit UI | Free | $0/month | 1 GB |
| **Total** | | **$0/month** | |

---

## Performance Expectations

### High Quality (NLLB on Starter)

- First translation: 45-60 seconds
- Cached translations: 3-5 seconds
- Quality: ⭐⭐⭐⭐⭐ (Google Translate-like)
- Concurrent users: 5-10

### Free Tier (MarianMT)

- First translation: 30-45 seconds
- Cached translations: 1-2 seconds
- Quality: ⭐⭐⭐ (Good, functional)
- Concurrent users: 2-3

---

## Updating Deployment

### Update Code

```bash
git add .
git commit -m "Update translation system"
git push origin main
```

Both Render and Streamlit will auto-deploy on push.

### Change Model Quality

**Switch to High Quality:**
```bash
python toggle_model.py nllb
git add core/config.py
git commit -m "Enable NLLB model"
git push
```

**Switch to Lightweight:**
```bash
python toggle_model.py marian
git add core/config.py
git commit -m "Enable MarianMT model"
git push
```

---

## Monitoring

### Render Dashboard
- View logs: Dashboard → Your Service → Logs
- Check metrics: Dashboard → Your Service → Metrics
- Monitor memory: Should stay under plan limit

### Streamlit Dashboard
- View logs: Streamlit Cloud → Your App → Logs
- Check usage: Streamlit Cloud → Your App → Analytics

---

## Quick Commands

### Deploy to Render (High Quality)
```bash
# 1. Update config for NLLB
python toggle_model.py nllb

# 2. Push to GitHub
git add .
git commit -m "Deploy with NLLB"
git push origin main

# 3. Create service on Render using render.yaml
# 4. Select Starter plan ($7/month)
```

### Deploy to Render (Free)
```bash
# 1. Update config for MarianMT
python toggle_model.py marian

# 2. Push to GitHub
git add .
git commit -m "Deploy with MarianMT"
git push origin main

# 3. Create service on Render using render-free.yaml
# 4. Select Free plan
```

### Deploy to Streamlit Cloud
```bash
# 1. Update API URL in ui/app.py
# 2. Push to GitHub
git add .
git commit -m "Configure Streamlit"
git push origin main

# 3. Deploy on share.streamlit.io
# 4. Point to streamlit_app.py
```

---

## Support

- **Render Docs**: https://render.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Your Docs**: See `TRANSLATION_QUALITY_GUIDE.md`

---

## Summary

**For Best Quality:**
1. Deploy API to Render Starter ($7/month) with NLLB
2. Deploy UI to Streamlit Cloud (free)
3. Total cost: $7/month

**For Free:**
1. Deploy API to Render Free with MarianMT
2. Deploy UI to Streamlit Cloud (free)
3. Total cost: $0/month

Both setups work great - choose based on your quality needs and budget! 🚀
