"""
Direct usage of the translation engine without API.
Useful for testing and understanding the core components.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.translator import translation_engine
from core.language_detector import language_detector
from core.model_manager import model_manager
from utils.memory import MemoryMonitor, log_memory_usage


def example_basic_translation():
    """Basic translation example."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Translation")
    print("=" * 60)
    
    with MemoryMonitor("Basic Translation"):
        result = translation_engine.translate(
            text="नमस्ते दुनिया",
            source_lang="hi",
            target_lang="en"
        )
    
    print(f"Success: {result['success']}")
    print(f"Input: नमस्ते दुनिया")
    print(f"Output: {result['translated_text']}")
    print(f"Method: {result['method']}")


def example_auto_detection():
    """Auto language detection example."""
    print("\n" + "=" * 60)
    print("Example 2: Auto Language Detection")
    print("=" * 60)
    
    texts = [
        "Hello world",
        "नमस्ते",
        "হ্যালো",
        "வணக்கம்",
        "నమస్కారం"
    ]
    
    for text in texts:
        detected = language_detector.detect(text)
        info = language_detector.get_language_info(text)
        print(f"Text: {text:20} → Detected: {detected:5} (Confidence: {info['confidence']})")


def example_english_bridge():
    """English-bridge translation example."""
    print("\n" + "=" * 60)
    print("Example 3: English-Bridge Translation")
    print("=" * 60)
    
    with MemoryMonitor("English-Bridge Translation"):
        result = translation_engine.translate(
            text="नमस्ते",
            source_lang="hi",
            target_lang="ta"
        )
    
    print(f"Hindi → Tamil (via English)")
    print(f"Input: नमस्ते")
    print(f"Output: {result['translated_text']}")
    print(f"Method: {result['method']}")


def example_batch_translation():
    """Batch translation example."""
    print("\n" + "=" * 60)
    print("Example 4: Batch Translation")
    print("=" * 60)
    
    texts = [
        "Good morning",
        "Thank you",
        "How are you?",
        "Welcome"
    ]
    
    with MemoryMonitor("Batch Translation"):
        results = translation_engine.batch_translate(
            texts=texts,
            source_lang="en",
            target_lang="hi"
        )
    
    for text, result in zip(texts, results):
        print(f"{text:20} → {result['translated_text']}")


def example_model_management():
    """Model management example."""
    print("\n" + "=" * 60)
    print("Example 5: Model Management")
    print("=" * 60)
    
    # Check initial state
    stats = model_manager.get_memory_stats()
    print(f"Initial models loaded: {stats['loaded_models']}")
    
    # Load first model
    print("\nTranslating Hindi → English...")
    translation_engine.translate("नमस्ते", "hi", "en")
    stats = model_manager.get_memory_stats()
    print(f"Models loaded: {stats['loaded_models']}")
    print(f"Model names: {stats['model_names']}")
    
    # Load second model
    print("\nTranslating Bengali → English...")
    translation_engine.translate("হ্যালো", "bn", "en")
    stats = model_manager.get_memory_stats()
    print(f"Models loaded: {stats['loaded_models']}")
    print(f"Model names: {stats['model_names']}")
    
    # Load third model (should evict oldest)
    print("\nTranslating Tamil → English...")
    translation_engine.translate("வணக்கம்", "ta", "en")
    stats = model_manager.get_memory_stats()
    print(f"Models loaded: {stats['loaded_models']}")
    print(f"Model names: {stats['model_names']}")
    
    # Unload all
    print("\nUnloading all models...")
    model_manager.unload_all_models()
    stats = model_manager.get_memory_stats()
    print(f"Models loaded: {stats['loaded_models']}")


def example_hinglish_detection():
    """Hinglish detection example."""
    print("\n" + "=" * 60)
    print("Example 6: Hinglish Detection")
    print("=" * 60)
    
    hinglish_texts = [
        "Aaj main market जा रहा हूं",
        "Yeh bahut अच्छा है",
        "Main kal आऊंगा"
    ]
    
    for text in hinglish_texts:
        is_hinglish = language_detector.detect_hinglish(text)
        detected = language_detector.detect(text)
        print(f"Text: {text}")
        print(f"  Is Hinglish: {is_hinglish}")
        print(f"  Detected as: {detected}")
        print()


def example_supported_pairs():
    """Show supported translation pairs."""
    print("\n" + "=" * 60)
    print("Example 7: Supported Translation Pairs")
    print("=" * 60)
    
    pairs = translation_engine.get_supported_pairs()
    
    # Group by source language
    from collections import defaultdict
    grouped = defaultdict(list)
    for pair in pairs:
        grouped[pair['source']].append(pair['target'])
    
    for source, targets in sorted(grouped.items())[:5]:  # Show first 5
        print(f"{source} → {', '.join(targets)}")
    
    print(f"\nTotal pairs: {len(pairs)}")


def example_memory_monitoring():
    """Memory monitoring example."""
    print("\n" + "=" * 60)
    print("Example 8: Memory Monitoring")
    print("=" * 60)
    
    log_memory_usage("[START]")
    
    # Perform translations
    for i in range(3):
        with MemoryMonitor(f"Translation {i+1}"):
            translation_engine.translate("Hello", "en", "hi")
    
    log_memory_usage("[END]")


def example_error_handling():
    """Error handling example."""
    print("\n" + "=" * 60)
    print("Example 9: Error Handling")
    print("=" * 60)
    
    # Empty text
    result = translation_engine.translate("", "en", "hi")
    print(f"Empty text: Success={result['success']}, Error={result.get('error')}")
    
    # Same source and target
    result = translation_engine.translate("Hello", "en", "en")
    print(f"Same language: Success={result['success']}, Method={result.get('method')}")
    
    # Unsupported pair (if any)
    result = translation_engine.translate("Hello", "en", "xx")
    print(f"Unsupported: Success={result['success']}, Error={result.get('error')}")


def example_health_check():
    """Health check example."""
    print("\n" + "=" * 60)
    print("Example 10: Health Check")
    print("=" * 60)
    
    health = translation_engine.health_check()
    
    print(f"Status: {health['status']}")
    print(f"Models Loaded: {health['models_loaded']}")
    print(f"Test Translation: {health['test_translation']}")
    print(f"Memory Stats: {health['memory_stats']}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("IndiaTranslate - Direct Usage Examples")
    print("=" * 60)
    
    # Run all examples
    example_basic_translation()
    example_auto_detection()
    example_english_bridge()
    example_batch_translation()
    example_model_management()
    example_hinglish_detection()
    example_supported_pairs()
    example_memory_monitoring()
    example_error_handling()
    example_health_check()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
