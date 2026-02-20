"""
Example usage of the IndiaTranslate API.
Demonstrates various translation scenarios.
"""

import requests
import json

# API endpoint (change to your deployed URL)
API_URL = "http://localhost:8000"


def translate_text(text, source_lang=None, target_lang="en", auto_detect=True):
    """Translate text using the API."""
    response = requests.post(
        f"{API_URL}/translate",
        json={
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "auto_detect": auto_detect
        }
    )
    return response.json()


def batch_translate(texts, source_lang=None, target_lang="en"):
    """Translate multiple texts."""
    response = requests.post(
        f"{API_URL}/batch-translate",
        json={
            "texts": texts,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    )
    return response.json()


def get_supported_languages():
    """Get list of supported languages."""
    response = requests.get(f"{API_URL}/languages")
    return response.json()


def check_health():
    """Check API health."""
    response = requests.get(f"{API_URL}/health")
    return response.json()


# Example 1: Auto-detect and translate to English
print("=" * 60)
print("Example 1: Auto-detect Hindi to English")
print("=" * 60)
result = translate_text("नमस्ते दुनिया", target_lang="en")
print(f"Input: नमस्ते दुनिया")
print(f"Output: {result['translated_text']}")
print(f"Detected: {result['source_lang']} → {result['target_lang']}")
print(f"Method: {result['method']}")
print()

# Example 2: English to Hindi
print("=" * 60)
print("Example 2: English to Hindi")
print("=" * 60)
result = translate_text("Hello, how are you?", source_lang="en", target_lang="hi")
print(f"Input: Hello, how are you?")
print(f"Output: {result['translated_text']}")
print(f"Method: {result['method']}")
print()

# Example 3: Bengali to Tamil (English-bridge)
print("=" * 60)
print("Example 3: Bengali to Tamil (via English bridge)")
print("=" * 60)
result = translate_text("হ্যালো বন্ধুরা", source_lang="bn", target_lang="ta")
print(f"Input: হ্যালো বন্ধুরা")
print(f"Output: {result['translated_text']}")
print(f"Method: {result['method']}")
print()

# Example 4: Batch translation
print("=" * 60)
print("Example 4: Batch Translation")
print("=" * 60)
texts = [
    "Good morning",
    "Thank you",
    "How are you?"
]
results = batch_translate(texts, source_lang="en", target_lang="hi")
for i, (text, result) in enumerate(zip(texts, results['results']), 1):
    print(f"{i}. {text} → {result['translated_text']}")
print()

# Example 5: Multiple Indian languages
print("=" * 60)
print("Example 5: Translate to Multiple Languages")
print("=" * 60)
text = "Welcome to India"
target_languages = ["hi", "bn", "ta", "te", "mr"]
for lang in target_languages:
    result = translate_text(text, source_lang="en", target_lang=lang)
    print(f"English → {lang}: {result['translated_text']}")
print()

# Example 6: Get supported languages
print("=" * 60)
print("Example 6: Supported Languages")
print("=" * 60)
languages = get_supported_languages()
print(f"Total languages: {languages['count']}")
for lang in languages['languages'][:5]:  # Show first 5
    print(f"  - {lang['name']} ({lang['code']})")
print("  ...")
print()

# Example 7: Health check
print("=" * 60)
print("Example 7: System Health")
print("=" * 60)
health = check_health()
print(f"Status: {health['status']}")
print(f"Memory Usage: {health['memory_usage_mb']} MB")
print(f"Models Loaded: {health['models_loaded']}")
print()

# Example 8: Error handling
print("=" * 60)
print("Example 8: Error Handling")
print("=" * 60)
try:
    # Empty text
    result = translate_text("", target_lang="hi")
    print(result)
except Exception as e:
    print(f"Error: {e}")
print()

# Example 9: Long text translation
print("=" * 60)
print("Example 9: Long Text Translation")
print("=" * 60)
long_text = """
India is a diverse country with many languages and cultures.
It has a rich history spanning thousands of years.
The country is known for its contributions to science, mathematics, and philosophy.
"""
result = translate_text(long_text.strip(), source_lang="en", target_lang="hi")
print(f"Input length: {len(long_text)} characters")
print(f"Output: {result['translated_text'][:100]}...")
print()

# Example 10: Hinglish detection
print("=" * 60)
print("Example 10: Hinglish Detection")
print("=" * 60)
hinglish_text = "Aaj main market जा रहा हूं"
result = translate_text(hinglish_text, target_lang="en")
print(f"Input: {hinglish_text}")
print(f"Output: {result['translated_text']}")
print(f"Detected: {result['source_lang']}")
print()

print("=" * 60)
print("All examples completed!")
print("=" * 60)
