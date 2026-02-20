# Simple Deployment Guide

## What You Need to Do

### For Render (API Backend)

**Choose One:**

**A) High Quality Translation ($7/month)**
```bash
1. Run: python toggle_model.py nllb
2. Push to GitHub
3. Deploy on Render with "Starter" plan
4. Set: USE_NLLB_MODEL=true
```

**B) Free Translation ($0/month)**
```bash
1. Run: python toggle_model.py marian
2. Push to GitHub
3. Deploy on Render with "Free" plan
4. Set: USE_NLLB_MODEL=false
```

### For Streamlit (UI Frontend)

```bash
1. Update ui/app.py with your Render API URL
2. Push to GitHub
3. Deploy on share.streamlit.io
4. Point to: streamlit_app.py
```

---

## Files You Need

### Already Created for You:

✅ `render.yaml` - For Render Starter plan (high quality)
✅ `render-free.yaml` - For Render Free plan (lightweight)
✅ `streamlit_app.py` - For Streamlit Cloud
✅ `.streamlit/config.toml` - Streamlit configuration

### You Just Need To:

1. **Choose quality level** (run toggle_model.py)
2. **Push to GitHub**
3. **Deploy on Render** (use render.yaml or render-free.yaml)
4. **Deploy on Streamlit** (use streamlit_app.py)

---

## Quick Commands

```bash
# Step 1: Choose model
python toggle_model.py nllb    # High quality
# OR
python toggle_model.py marian  # Lightweight

# Step 2: Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# Step 3 & 4: Deploy via web dashboards
# Render: https://dashboard.render.com
# Streamlit: https://share.streamlit.io
```

---

## That's It!

Everything is configured and ready. Just:
1. Choose your plan
2. Push to GitHub
3. Click deploy on both platforms

See `DEPLOYMENT_GUIDE.md` for detailed step-by-step instructions.
See `DEPLOY_CHECKLIST.md` for a complete checklist.
