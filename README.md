# 🌐 IndiaTranslate - Production AI Translation System

A production-grade multilingual AI translation platform supporting 13+ Indian languages using transformer-based models, optimized for low-resource deployment.

## ✨ Translation Quality

**Two Model Options:**

1. **NLLB-200 (Default)** - Google Translate-like quality
   - Facebook's state-of-the-art multilingual model
   - Supports 200+ languages with direct translation
   - Higher accuracy and fluency
   - Memory: ~1.2 GB

2. **MarianMT (Lightweight)** - Fast and efficient
   - Helsinki-NLP lightweight models
   - Lower memory footprint
   - Memory: ~300-500 MB

**Switch models easily:**
```bash
python toggle_model.py nllb    # High quality
python toggle_model.py marian  # Lightweight
```

## 🎯 Key Features

- **13+ Indian Languages**: Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Odia, Assamese, Sanskrit + English
- **Transformer-Based**: Facebook NLLB-200 or HuggingFace MarianMT
- **High Quality**: Beam search, length penalty, repetition prevention
- **Memory-Optimized**: Runs on 512MB-1.5GB RAM depending on model
- **Smart Routing**: Direct translation with automatic fallback
- **Auto Language Detection**: Automatic source language identification
- **Production Ready**: FastAPI backend + Streamlit frontend

## 🏗️ Architecture

```
├── core/                    # Translation engine
│   ├── translator.py       # Main translation logic
│   ├── model_manager.py    # Dynamic model loading
│   ├── language_detector.py # Auto-detection
│   └── config.py           # Model configurations
├── api/                     # FastAPI backend
│   └── main.py             # REST endpoints
├── ui/                      # Streamlit frontend
│   └── app.py              # Web interface
├── utils/                   # Utilities
│   ├── memory.py           # Memory optimization
│   └── logger.py           # Logging
├── requirements.txt         # Dependencies
└── render.yaml             # Deployment config
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Run UI (separate terminal)
streamlit run ui/app.py --server.port 8501
```

## 💾 Memory Optimization & Quality Settings

- **Lazy Loading**: Models loaded only when needed
- **Dynamic Unloading**: Automatic memory cleanup
- **8-bit Quantization**: Reduces memory by ~50%
- **Beam Search**: 5 beams for better translation quality
- **Length Penalty**: Balanced output length
- **Repetition Prevention**: No repeated phrases
- **CPU Optimized**: No GPU required
- **Smart Caching**: LRU cache for frequent pairs

## 🌍 Supported Languages

Hindi (hi), Bengali (bn), Tamil (ta), Telugu (te), Marathi (mr), Gujarati (gu), Kannada (kn), Malayalam (ml), Punjabi (pa), Urdu (ur), Odia (or), Assamese (as), Sanskrit (sa), English (en)

## 📊 Performance

- **Memory Usage**: ~400-500 MB
- **Translation Speed**: 1-3 seconds per sentence
- **Accuracy**: Comparable to commercial APIs
- **Scalability**: Horizontal scaling ready

## 🔧 Deployment

### Render (Free Tier)

1. Connect GitHub repository
2. Select "Web Service"
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

See `DEPLOYMENT.md` for detailed instructions.

## 📝 API Usage

```python
import requests

response = requests.post("http://localhost:8000/translate", json={
    "text": "नमस्ते दुनिया",
    "source_lang": "hi",
    "target_lang": "en"
})
print(response.json()["translated_text"])
```

## 🎓 Technical Highlights

- **NLP/ML**: Transformer models, quantization, memory optimization
- **Backend**: FastAPI, async processing, rate limiting
- **Frontend**: Streamlit, responsive UI, translation history
- **DevOps**: Production deployment, monitoring, error handling

## 📄 License

MIT License - See LICENSE file for details
