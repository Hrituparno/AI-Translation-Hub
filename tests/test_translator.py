"""
Unit tests for translation engine.
Run with: pytest tests/test_translator.py
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.translator import translation_engine
from core.language_detector import language_detector
from core.model_manager import model_manager


class TestLanguageDetector:
    """Test language detection functionality."""
    
    def test_detect_hindi(self):
        """Test Hindi detection."""
        text = "नमस्ते दुनिया"
        detected = language_detector.detect(text)
        assert detected == "hi"
    
    def test_detect_english(self):
        """Test English detection."""
        text = "Hello world"
        detected = language_detector.detect(text)
        assert detected == "en"
    
    def test_detect_bengali(self):
        """Test Bengali detection."""
        text = "হ্যালো বিশ্ব"
        detected = language_detector.detect(text)
        assert detected == "bn"
    
    def test_detect_tamil(self):
        """Test Tamil detection."""
        text = "வணக்கம் உலகம்"
        detected = language_detector.detect(text)
        assert detected == "ta"
    
    def test_detect_hinglish(self):
        """Test Hinglish detection."""
        text = "Aaj main market जा रहा हूं"
        is_hinglish = language_detector.detect_hinglish(text)
        assert is_hinglish is True
    
    def test_detect_empty(self):
        """Test empty text detection."""
        detected = language_detector.detect("")
        assert detected == "en"  # Default


class TestModelManager:
    """Test model management functionality."""
    
    def test_get_model_name(self):
        """Test model name retrieval."""
        model_name = model_manager.get_model_name("hi", "en")
        assert model_name is not None
        assert "Helsinki-NLP" in model_name
    
    def test_unsupported_pair(self):
        """Test unsupported language pair."""
        model_name = model_manager.get_model_name("xx", "yy")
        assert model_name is None
    
    def test_memory_stats(self):
        """Test memory statistics."""
        stats = model_manager.get_memory_stats()
        assert "loaded_models" in stats
        assert "model_names" in stats
        assert "max_models" in stats


class TestTranslationEngine:
    """Test translation engine functionality."""
    
    def test_same_language(self):
        """Test translation with same source and target."""
        result = translation_engine.translate(
            text="Hello",
            source_lang="en",
            target_lang="en"
        )
        assert result["success"] is True
        assert result["translated_text"] == "Hello"
        assert result["method"] == "no_translation_needed"
    
    def test_empty_text(self):
        """Test translation with empty text."""
        result = translation_engine.translate(
            text="",
            source_lang="en",
            target_lang="hi"
        )
        assert result["success"] is False
        assert "error" in result
    
    def test_auto_detect(self):
        """Test auto language detection."""
        result = translation_engine.translate(
            text="नमस्ते",
            source_lang=None,
            target_lang="en",
            auto_detect=True
        )
        assert result["success"] is True
        assert result["source_lang"] == "hi"
    
    def test_supported_pairs(self):
        """Test getting supported pairs."""
        pairs = translation_engine.get_supported_pairs()
        assert len(pairs) > 0
        assert all("source" in p and "target" in p for p in pairs)
    
    def test_health_check(self):
        """Test health check."""
        health = translation_engine.health_check()
        assert "status" in health
        assert "models_loaded" in health


class TestBatchTranslation:
    """Test batch translation functionality."""
    
    def test_batch_translate(self):
        """Test batch translation."""
        texts = ["Hello", "World"]
        results = translation_engine.batch_translate(
            texts=texts,
            source_lang="en",
            target_lang="hi"
        )
        assert len(results) == len(texts)
        assert all("success" in r for r in results)
    
    def test_empty_batch(self):
        """Test empty batch."""
        results = translation_engine.batch_translate(
            texts=[],
            source_lang="en",
            target_lang="hi"
        )
        assert len(results) == 0


# Integration tests (require model downloads)
@pytest.mark.integration
class TestIntegration:
    """Integration tests with actual models."""
    
    def test_english_to_hindi(self):
        """Test English to Hindi translation."""
        result = translation_engine.translate(
            text="Hello",
            source_lang="en",
            target_lang="hi"
        )
        assert result["success"] is True
        assert result["translated_text"] is not None
        assert len(result["translated_text"]) > 0
    
    def test_hindi_to_english(self):
        """Test Hindi to English translation."""
        result = translation_engine.translate(
            text="नमस्ते",
            source_lang="hi",
            target_lang="en"
        )
        assert result["success"] is True
        assert result["translated_text"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
