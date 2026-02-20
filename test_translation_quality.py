"""
Test script to verify translation quality improvements.
Tests both NLLB and MarianMT models.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.translator import translation_engine
from core.config import USE_NLLB_MODEL

def test_translations():
    """Test various translation scenarios."""
    
    print("=" * 60)
    print(f"Translation Quality Test")
    print(f"Using NLLB Model: {USE_NLLB_MODEL}")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "text": "Hello, how are you?",
            "source": "en",
            "target": "hi",
            "expected_contains": ["नमस्ते", "कैसे", "हो"]
        },
        {
            "text": "I love programming",
            "source": "en",
            "target": "hi",
            "expected_contains": ["प्रोग्रामिंग", "पसंद"]
        },
        {
            "text": "Good morning",
            "source": "en",
            "target": "ta",
            "expected_contains": ["காலை", "வணக்கம்"]
        },
        {
            "text": "Thank you very much",
            "source": "en",
            "target": "bn",
            "expected_contains": ["ধন্যবাদ"]
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"  Input: {test['text']}")
        print(f"  {test['source']} -> {test['target']}")
        
        result = translation_engine.translate(
            text=test['text'],
            source_lang=test['source'],
            target_lang=test['target'],
            auto_detect=False
        )
        
        if result['success']:
            print(f"  Output: {result['translated_text']}")
            print(f"  Method: {result.get('method', 'unknown')}")
            results.append({
                "test": i,
                "success": True,
                "output": result['translated_text']
            })
        else:
            print(f"  ERROR: {result.get('error', 'Unknown error')}")
            results.append({
                "test": i,
                "success": False,
                "error": result.get('error')
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    successful = sum(1 for r in results if r['success'])
    print(f"  Successful: {successful}/{len(test_cases)}")
    print(f"  Failed: {len(test_cases) - successful}/{len(test_cases)}")
    print("=" * 60)
    
    # Memory stats
    memory_stats = translation_engine.model_manager.get_memory_stats()
    print(f"\nMemory Stats:")
    print(f"  Models loaded: {memory_stats['loaded_models']}")
    print(f"  Model names: {memory_stats['model_names']}")

if __name__ == "__main__":
    try:
        test_translations()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
