# 🚀 Deployment Guide - IndiaTranslate

Complete guide for deploying the AI translation system to production environments.

## 📋 Prerequisites

- Python 3.9+
- Git
- 512MB+ RAM (optimized for Render Free Tier)
- CPU-only environment supported

## 🔧 Local Development Setup

### 1. Clone and Install

```bash
# Clone repository
git clone <your-repo-url>
cd india-translate

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Backend API

```bash
# Start FastAPI server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Run Frontend UI

```bash
# In a new terminal, activate venv and run
streamlit run ui/app.py --server.port 8501

# UI will be available at http://localhost:8501
```

### 4. Test the System

```bash
# Test API endpoint
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "source_lang": "en", "target_lang": "hi"}'

# Check health
curl http://localhost:8000/health
```

## ☁️ Render Deployment (Recommended for Free Tier)

### Option 1: Deploy API Backend

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `india-translate-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: `Free` (512MB RAM)

3. **Environment Variables** (Optional)
   ```
   LOG_LEVEL=INFO
   MAX_MODELS_IN_MEMORY=2
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Models will download on first request (be patient!)

### Option 2: Deploy Streamlit UI

1. **Create Another Web Service**
   - **Name**: `india-translate-ui`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run ui/app.py --server.port $PORT --server.address 0.0.0.0`

2. **Environment Variables**
   ```
   API_URL=https://india-translate-api.onrender.com
   ```

### Using render.yaml (Automated)

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: india-translate-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
    plan: free
    healthCheckPath: /health
    envVars:
      - key: LOG_LEVEL
        value: INFO
      - key: MAX_MODELS_IN_MEMORY
        value: 2
```

Then deploy via Render Dashboard → "New" → "Blueprint" → Connect repo.

## 🐳 Alternative: Railway Deployment

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

Railway will auto-detect Python and use:
- Build: `pip install -r requirements.txt`
- Start: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

## 🔍 Production Considerations

### Memory Optimization

The system is optimized for 512MB RAM:

1. **Lazy Model Loading**: Models load only when needed
2. **LRU Eviction**: Old models unloaded automatically
3. **CPU-Only**: No GPU required
4. **Quantization Ready**: Enable in `core/config.py`

### First Request Latency

- First translation takes 30-60 seconds (model download)
- Subsequent requests: 1-3 seconds
- Models cached on disk after first download

### Scaling Strategies

**Horizontal Scaling** (Multiple instances):
```bash
# Each instance handles different language pairs
# Use load balancer to distribute requests
```

**Vertical Scaling** (More RAM):
```python
# In core/config.py
MAX_MODELS_IN_MEMORY = 5  # Load more models
ENABLE_QUANTIZATION = False  # Use full precision
```

**GPU Acceleration** (Future):
```python
# In core/model_manager.py
self.device = "cuda" if torch.cuda.is_available() else "cpu"
```

## 📊 Monitoring

### Health Check Endpoint

```bash
curl https://your-app.onrender.com/health
```

Response:
```json
{
  "status": "healthy",
  "models_loaded": 2,
  "memory_usage_mb": 456.78,
  "supported_languages": 14
}
```

### Memory Monitoring

```bash
curl https://your-app.onrender.com/memory
```

### Logs

- Render: Dashboard → Service → Logs
- Railway: `railway logs`
- Local: Check console output

## 🐛 Troubleshooting

### Issue: Out of Memory

**Solution**:
```python
# In core/config.py
MAX_MODELS_IN_MEMORY = 1  # Reduce to 1 model
MAX_INPUT_LENGTH = 256    # Reduce token limit
```

### Issue: Slow First Request

**Expected behavior**: Models download on first use
- Wait 30-60 seconds for first translation
- Subsequent requests will be fast

### Issue: Translation Fails

**Check**:
1. Health endpoint: `/health`
2. Supported pairs: `/translation-pairs`
3. Logs for error messages

### Issue: API Connection Error (UI)

**Solution**:
- Update API URL in Streamlit sidebar
- Ensure backend is running
- Check CORS settings in `api/main.py`

## 🔐 Security Best Practices

1. **Rate Limiting**: Already implemented (100 req/min)
2. **Input Validation**: Pydantic models validate all inputs
3. **CORS**: Configure allowed origins in production
4. **API Keys**: Add authentication for production use

```python
# In api/main.py
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/translate")
async def translate(request: TranslationRequest, api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    # ... rest of code
```

## 📈 Performance Benchmarks

**Render Free Tier (512MB RAM, CPU)**:
- Memory Usage: 400-500 MB
- Translation Speed: 1-3 seconds
- Concurrent Requests: 2-3
- Uptime: 99%+ (sleeps after 15min inactivity)

**Recommended Paid Tier (2GB RAM)**:
- Memory Usage: 800-1200 MB
- Translation Speed: 0.5-1 second
- Concurrent Requests: 10+
- Models in Memory: 5+

## 🎯 Next Steps

1. **Add Authentication**: Implement API keys
2. **Database**: Store translation history
3. **Caching**: Redis for frequent translations
4. **CDN**: CloudFlare for static assets
5. **Monitoring**: Sentry for error tracking
6. **Analytics**: Track usage patterns

## 📞 Support

For issues or questions:
- Check logs first
- Review this guide
- Open GitHub issue
- Check HuggingFace model status

## 📄 License

MIT License - See LICENSE file
