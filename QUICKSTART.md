# ⚡ Quick Start Guide - IndiaTranslate

Get up and running in 5 minutes!

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd india-translate
```

### Step 2: Create Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyTorch (ML framework)
- Transformers (HuggingFace)
- FastAPI (Backend)
- Streamlit (Frontend)
- Other utilities

**Note**: First installation may take 5-10 minutes.

## 🎯 Running the Application

### Option 1: Using Startup Scripts (Recommended)

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

This starts both API and UI automatically!

### Option 2: Manual Start

**Terminal 1 - API Server:**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - UI Server:**
```bash
streamlit run ui/app.py --server.port 8501
```

## 🌐 Access the Application

Once started, open your browser:

- **Web UI**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📝 First Translation

### Using the Web UI

1. Open http://localhost:8501
2. Enter text in the input box
3. Select target language
4. Click "Translate"
5. Wait 30-60 seconds for first translation (model download)
6. Subsequent translations will be fast (1-3 seconds)

### Using the API

```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "source_lang": "en",
    "target_lang": "hi"
  }'
```

Response:
```json
{
  "success": true,
  "translated_text": "नमस्कार दुनिया",
  "source_lang": "en",
  "target_lang": "hi",
  "method": "direct"
}
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/translate",
    json={
        "text": "नमस्ते दुनिया",
        "target_lang": "en"
    }
)

print(response.json()["translated_text"])
# Output: Hello world
```

## 🎨 Example Translations

### Auto-Detect Language

```python
# API automatically detects Hindi
{
  "text": "नमस्ते",
  "target_lang": "en"
}
# → "Hello"
```

### English to Multiple Languages

```python
# English to Hindi
{"text": "Hello", "source_lang": "en", "target_lang": "hi"}
# → "नमस्कार"

# English to Bengali
{"text": "Hello", "source_lang": "en", "target_lang": "bn"}
# → "হ্যালো"

# English to Tamil
{"text": "Hello", "source_lang": "en", "target_lang": "ta"}
# → "வணக்கம்"
```

### Indian Language to Indian Language

```python
# Hindi to Tamil (via English bridge)
{"text": "नमस्ते", "source_lang": "hi", "target_lang": "ta"}
# → "வணக்கம்"
```

### Batch Translation

```python
{
  "texts": ["Hello", "Thank you", "Welcome"],
  "source_lang": "en",
  "target_lang": "hi"
}
# → ["नमस्कार", "धन्यवाद", "स्वागत"]
```

## 🔍 Testing

### Run Unit Tests

```bash
pip install pytest
pytest tests/test_translator.py -v
```

### Run Example Scripts

```bash
# Direct usage examples
python examples/direct_usage.py

# API usage examples (requires API running)
python examples/api_usage.py
```

## 📊 Monitoring

### Check System Health

```bash
curl http://localhost:8000/health
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

### Check Memory Usage

```bash
curl http://localhost:8000/memory
```

### View Logs

Logs appear in the terminal where you started the servers.

## 🐛 Troubleshooting

### Issue: "Module not found"

**Solution**: Make sure virtual environment is activated
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Issue: "Port already in use"

**Solution**: Change the port
```bash
uvicorn api.main:app --port 8001
streamlit run ui/app.py --server.port 8502
```

### Issue: "Out of memory"

**Solution**: Reduce models in memory
```python
# In core/config.py
MAX_MODELS_IN_MEMORY = 1
```

### Issue: First translation is slow

**Expected**: First translation takes 30-60 seconds to download models. This is normal! Subsequent translations will be fast.

### Issue: Translation fails

**Check**:
1. Is the API running? Visit http://localhost:8000/health
2. Is the language pair supported? Visit http://localhost:8000/translation-pairs
3. Check logs for error messages

## 🌍 Supported Languages

| Language | Code | To English | From English |
|----------|------|------------|--------------|
| English | en | N/A | N/A |
| Hindi | hi | ✅ | ✅ |
| Bengali | bn | ✅ | ✅ |
| Tamil | ta | ✅ | ✅ |
| Telugu | te | ✅ | ✅ |
| Marathi | mr | ✅ | ✅ |
| Gujarati | gu | ✅ | ✅ |
| Kannada | kn | ✅ | ✅ |
| Malayalam | ml | ✅ | ✅ |
| Punjabi | pa | ✅ | ✅ |
| Urdu | ur | ✅ | ✅ |
| Odia | or | ✅ | ✅ |
| Assamese | as | ✅ | ✅ |
| Sanskrit | sa | ✅ | ✅ |

**Note**: Any language to any language is supported via English-bridge translation.

## 📚 Next Steps

1. **Read Documentation**:
   - [README.md](README.md) - Project overview
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
   - [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) - Deep dive

2. **Explore Examples**:
   - `examples/api_usage.py` - API examples
   - `examples/direct_usage.py` - Direct engine usage

3. **Deploy to Cloud**:
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md) for Render/Railway

4. **Customize**:
   - Modify `core/config.py` for settings
   - Add new models in `MODEL_MAPPINGS`
   - Adjust memory limits

## 💡 Tips

1. **First Run**: Be patient! Model downloads take time.
2. **Memory**: Monitor with `/memory` endpoint
3. **Performance**: Use direct language pairs when possible
4. **Caching**: Models are cached after first download
5. **Logs**: Check terminal output for debugging

## 🎯 Common Use Cases

### 1. Translate Website Content

```python
import requests

def translate_content(text, target_lang):
    response = requests.post(
        "http://localhost:8000/translate",
        json={"text": text, "target_lang": target_lang}
    )
    return response.json()["translated_text"]

# Translate to multiple languages
content = "Welcome to our website"
for lang in ["hi", "bn", "ta"]:
    print(f"{lang}: {translate_content(content, lang)}")
```

### 2. Batch Process Documents

```python
# Read document
with open("document.txt") as f:
    lines = f.readlines()

# Translate all lines
response = requests.post(
    "http://localhost:8000/batch-translate",
    json={"texts": lines, "target_lang": "hi"}
)

# Save translated document
with open("document_hi.txt", "w") as f:
    for result in response.json()["results"]:
        f.write(result["translated_text"] + "\n")
```

### 3. Real-time Chat Translation

```python
def translate_message(message, user_lang):
    response = requests.post(
        "http://localhost:8000/translate",
        json={"text": message, "target_lang": user_lang}
    )
    return response.json()["translated_text"]

# User sends message in Hindi
user_message = "मुझे मदद चाहिए"
english_message = translate_message(user_message, "en")
print(f"User said: {english_message}")

# Reply in user's language
reply = "How can I help you?"
hindi_reply = translate_message(reply, "hi")
print(f"Reply: {hindi_reply}")
```

## 🎉 You're Ready!

You now have a fully functional AI translation system running locally. Explore the API, try different languages, and check out the documentation for advanced features!

**Questions?** Check the documentation or open an issue on GitHub.

**Happy Translating! 🌐**
