"""
Configuration for translation models and language mappings.
Optimized for low-memory environments using lightweight MarianMT models.
"""

# Language code mappings
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

# Translation model configuration
# Using Facebook's NLLB-200 distilled model for better quality
# This is a 600M parameter model that supports 200+ languages including all Indian languages
USE_NLLB_MODEL = True  # Set to False to use MarianMT models

# NLLB language codes (different from ISO codes)
NLLB_LANG_CODES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "bn": "ben_Beng",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "mr": "mar_Deva",
    "gu": "guj_Gujr",
    "kn": "kan_Knda",
    "ml": "mal_Mlym",
    "pa": "pan_Guru",
    "ur": "urd_Arab",
    "or": "ory_Orya",
    "as": "asm_Beng",
    "sa": "san_Deva"
}

# NLLB model (better quality, supports all languages directly)
NLLB_MODEL_NAME = "facebook/nllb-200-distilled-600M"

# Lightweight MarianMT models from Helsinki-NLP (fallback)
# These are small, efficient models suitable for CPU and low memory
MODEL_MAPPINGS = {
    # Indian languages to English (most critical)
    ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",
    ("bn", "en"): "Helsinki-NLP/opus-mt-bn-en",
    ("ta", "en"): "Helsinki-NLP/opus-mt-ta-en",
    ("te", "en"): "Helsinki-NLP/opus-mt-te-en",
    ("mr", "en"): "Helsinki-NLP/opus-mt-mr-en",
    ("gu", "en"): "Helsinki-NLP/opus-mt-gu-en",
    ("ur", "en"): "Helsinki-NLP/opus-mt-ur-en",
    
    # English to Indian languages
    ("en", "hi"): "Helsinki-NLP/opus-mt-en-hi",
    ("en", "bn"): "Helsinki-NLP/opus-mt-en-bn",
    ("en", "ta"): "Helsinki-NLP/opus-mt-en-ta",
    ("en", "te"): "Helsinki-NLP/opus-mt-en-te",
    ("en", "mr"): "Helsinki-NLP/opus-mt-en-mr",
    ("en", "gu"): "Helsinki-NLP/opus-mt-en-gu",
    ("en", "ur"): "Helsinki-NLP/opus-mt-en-ur",
    
    # Grouped models for languages without direct pairs
    ("ml", "en"): "Helsinki-NLP/opus-mt-mul-en",  # Multilingual to English
    ("kn", "en"): "Helsinki-NLP/opus-mt-mul-en",
    ("pa", "en"): "Helsinki-NLP/opus-mt-mul-en",
    ("or", "en"): "Helsinki-NLP/opus-mt-mul-en",
    ("as", "en"): "Helsinki-NLP/opus-mt-mul-en",
    ("sa", "en"): "Helsinki-NLP/opus-mt-mul-en",
    
    ("en", "ml"): "Helsinki-NLP/opus-mt-en-mul",  # English to multilingual
    ("en", "kn"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "pa"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "or"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "as"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "sa"): "Helsinki-NLP/opus-mt-en-mul",
}

# Memory optimization settings
MAX_MODELS_IN_MEMORY = 1  # Keep only 1 model loaded (NLLB is larger)
MODEL_CACHE_SIZE = 1  # LRU cache size
MAX_INPUT_LENGTH = 512  # Token limit for memory efficiency
BATCH_SIZE = 1  # Process one at a time for memory safety

# Translation settings
USE_ENGLISH_BRIDGE = False  # Not needed with NLLB (supports direct translation)
AUTO_DETECT_LANGUAGE = True  # Enable automatic language detection
ENABLE_QUANTIZATION = True  # Enable 8-bit quantization for memory efficiency

# Translation quality settings (Google Translate-like)
NUM_BEAMS = 5  # Beam search width (higher = better quality, slower)
LENGTH_PENALTY = 1.0  # Length penalty for beam search
NO_REPEAT_NGRAM_SIZE = 3  # Prevent repetition
EARLY_STOPPING = True  # Stop when all beams finish

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# API settings
API_RATE_LIMIT = 100  # Requests per minute
API_TIMEOUT = 30  # Seconds

# Supported languages list
SUPPORTED_LANGUAGES = list(LANGUAGE_CODES.values())
