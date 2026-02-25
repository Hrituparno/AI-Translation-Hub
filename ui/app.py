"""
Streamlit frontend for IndiaTranslate.
Clean, responsive UI with translation history.
"""

import streamlit as st
import requests
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Language configuration (inline to avoid import issues on Streamlit Cloud)
LANGUAGE_CODES = {
    "english": "en",
    "hindi": "hi",
    "bengali": "bn",
    "tamil": "ta",
    "telugu": "te",
    "marathi": "mr",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "punjabi": "pa",
    "urdu": "ur",
    "odia": "or",
    "assamese": "as",
    "sanskrit": "sa"
}

LANGUAGE_NAMES = {v: k.title() for k, v in LANGUAGE_CODES.items()}
SUPPORTED_LANGUAGES = list(LANGUAGE_CODES.values())

# Page configuration
st.set_page_config(
    page_title="IndiaTranslate",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .translation-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .history-item {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'api_url' not in st.session_state:
    # Get API URL from environment variable or use default
    st.session_state.api_url = os.getenv("API_URL", "http://localhost:8000")

# Header
st.markdown('<div class="main-header">🌐 IndiaTranslate</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">AI-Powered Translation for 13+ Indian Languages</div>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API URL configuration
    api_url = st.text_input(
        "API URL",
        value=st.session_state.api_url,
        help="Backend API endpoint"
    )
    st.session_state.api_url = api_url
    
    # Auto-detect toggle
    auto_detect = st.checkbox("Auto-detect source language", value=True)
    
    st.divider()
    
    # System info
    st.header("📊 System Info")
    
    if st.button("Check Health"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                st.success(f"Status: {health['status']}")
                st.info(f"Memory: {health['memory_usage_mb']} MB")
                st.info(f"Models Loaded: {health['models_loaded']}")
            else:
                st.error("API unhealthy")
        except Exception as e:
            st.error(f"Cannot connect to API: {e}")
    
    st.divider()
    
    # Clear history
    if st.button("Clear History"):
        st.session_state.history = []
        st.success("History cleared!")

# Main translation interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Input")
    
    # Source language selection
    if not auto_detect:
        source_lang_name = st.selectbox(
            "Source Language",
            options=[LANGUAGE_NAMES.get(code, code) for code in SUPPORTED_LANGUAGES],
            index=SUPPORTED_LANGUAGES.index("en")
        )
        source_lang = [code for code, name in LANGUAGE_NAMES.items() if name == source_lang_name][0]
    else:
        source_lang = None
        st.info("🔍 Auto-detection enabled")
    
    # Input text
    input_text = st.text_area(
        "Enter text to translate",
        height=200,
        placeholder="Type or paste your text here..."
    )

with col2:
    st.subheader("🎯 Output")
    
    # Target language selection
    target_lang_name = st.selectbox(
        "Target Language",
        options=[LANGUAGE_NAMES.get(code, code) for code in SUPPORTED_LANGUAGES],
        index=SUPPORTED_LANGUAGES.index("hi")
    )
    target_lang = [code for code, name in LANGUAGE_NAMES.items() if name == target_lang_name][0]
    
    # Output placeholder
    output_placeholder = st.empty()

# Translate button
st.divider()
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    translate_button = st.button("🔄 Translate", use_container_width=True, type="primary")

# Translation logic
if translate_button:
    if not input_text.strip():
        st.error("Please enter text to translate")
    else:
        with st.spinner("Translating..."):
            try:
                # Call API
                response = requests.post(
                    f"{api_url}/translate",
                    json={
                        "text": input_text,
                        "source_lang": source_lang,
                        "target_lang": target_lang,
                        "auto_detect": auto_detect
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display translation
                    with output_placeholder.container():
                        st.markdown(
                            f'<div class="translation-box">{result["translated_text"]}</div>',
                            unsafe_allow_html=True
                        )
                        
                        # Metadata
                        st.caption(
                            f"🔤 {LANGUAGE_NAMES.get(result['source_lang'], result['source_lang'])} → "
                            f"{LANGUAGE_NAMES.get(result['target_lang'], result['target_lang'])} | "
                            f"Method: {result.get('method', 'N/A')}"
                        )
                    
                    # Add to history
                    st.session_state.history.insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "input": input_text[:100] + "..." if len(input_text) > 100 else input_text,
                        "output": result["translated_text"][:100] + "..." if len(result["translated_text"]) > 100 else result["translated_text"],
                        "source": result["source_lang"],
                        "target": result["target_lang"],
                        "method": result.get("method", "N/A")
                    })
                    
                    # Keep only last 10 items
                    st.session_state.history = st.session_state.history[:10]
                    
                    st.success("Translation completed!")
                    
                else:
                    st.error(f"Translation failed: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.Timeout:
                st.error("Translation timeout. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Make sure the backend is running.")
            except Exception as e:
                st.error(f"Error: {e}")

# Translation history
if st.session_state.history:
    st.divider()
    st.subheader("📜 Translation History")
    
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"{item['timestamp']} - {LANGUAGE_NAMES.get(item['source'], item['source'])} → {LANGUAGE_NAMES.get(item['target'], item['target'])}"):
            st.markdown(f"**Input:** {item['input']}")
            st.markdown(f"**Output:** {item['output']}")
            st.caption(f"Method: {item['method']}")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Built with ❤️ using HuggingFace Transformers, FastAPI, and Streamlit</p>
        <p>Supports: Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, Odia, Assamese, Sanskrit, English</p>
    </div>
    """,
    unsafe_allow_html=True
)
