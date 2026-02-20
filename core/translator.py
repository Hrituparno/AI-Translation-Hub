"""
Main translation engine with English-bridge fallback logic.
Orchestrates model manager and language detector.
"""

import logging
from typing import Optional, Dict, Any

from core.model_manager import model_manager
from core.language_detector import language_detector
from core.config import USE_ENGLISH_BRIDGE, AUTO_DETECT_LANGUAGE, USE_NLLB_MODEL

logger = logging.getLogger(__name__)


class TranslationEngine:
    """
    Core translation engine with intelligent routing.
    Supports direct translation and English-bridge fallback.
    """
    
    def __init__(self):
        self.model_manager = model_manager
        self.language_detector = language_detector
    
    def translate(
        self,
        text: str,
        source_lang: Optional[str] = None,
        target_lang: str = "en",
        auto_detect: bool = True
    ) -> Dict[str, Any]:
        """
        Translate text with automatic language detection and fallback.
        
        Args:
            text: Input text to translate
            source_lang: Source language code (auto-detected if None)
            target_lang: Target language code
            auto_detect: Enable automatic language detection
            
        Returns:
            Dictionary with translation results and metadata
        """
        if not text or not text.strip():
            return {
                "success": False,
                "error": "Empty input text",
                "translated_text": None
            }
        
        # Auto-detect source language if not provided
        if not source_lang and auto_detect and AUTO_DETECT_LANGUAGE:
            source_lang = self.language_detector.detect(text)
            logger.info(f"Auto-detected source language: {source_lang}")
        elif not source_lang:
            source_lang = "en"  # Default to English
        
        # Check if source and target are the same
        if source_lang == target_lang:
            return {
                "success": True,
                "translated_text": text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "method": "no_translation_needed"
            }
        
        # Try direct translation first
        translated = self._translate_direct(text, source_lang, target_lang)
        
        if translated:
            method = "nllb" if USE_NLLB_MODEL else "direct"
            return {
                "success": True,
                "translated_text": translated,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "method": method
            }
        
        # Fallback to English bridge if enabled (only for MarianMT)
        if USE_ENGLISH_BRIDGE and not USE_NLLB_MODEL and source_lang != "en" and target_lang != "en":
            logger.info(f"Attempting English-bridge translation: {source_lang} -> en -> {target_lang}")
            translated = self._translate_via_english(text, source_lang, target_lang)
            
            if translated:
                return {
                    "success": True,
                    "translated_text": translated,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "method": "english_bridge"
                }
        
        # Translation failed
        return {
            "success": False,
            "error": f"No translation model available for {source_lang} -> {target_lang}",
            "translated_text": None,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    
    def _translate_direct(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """Attempt direct translation between language pair."""
        try:
            return self.model_manager.translate(text, source_lang, target_lang)
        except Exception as e:
            logger.error(f"Direct translation failed: {e}")
            return None
    
    def _translate_via_english(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """
        Translate via English as pivot language.
        source_lang -> English -> target_lang
        """
        try:
            # Step 1: Translate to English
            english_text = self.model_manager.translate(text, source_lang, "en")
            
            if not english_text:
                logger.warning("Failed to translate to English")
                return None
            
            logger.info(f"Intermediate English: {english_text}")
            
            # Step 2: Translate from English to target
            final_text = self.model_manager.translate(english_text, "en", target_lang)
            
            return final_text
            
        except Exception as e:
            logger.error(f"English-bridge translation failed: {e}")
            return None
    
    def batch_translate(
        self,
        texts: list,
        source_lang: Optional[str] = None,
        target_lang: str = "en"
    ) -> list:
        """
        Translate multiple texts.
        
        Args:
            texts: List of input texts
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translation results
        """
        results = []
        
        for text in texts:
            result = self.translate(text, source_lang, target_lang)
            results.append(result)
        
        return results
    
    def get_supported_pairs(self) -> list:
        """Get list of supported translation pairs."""
        from core.config import MODEL_MAPPINGS
        
        pairs = []
        for (src, tgt), model in MODEL_MAPPINGS.items():
            pairs.append({
                "source": src,
                "target": tgt,
                "model": model
            })
        
        return pairs
    
    def health_check(self) -> Dict[str, Any]:
        """Check system health and readiness."""
        try:
            # Test a simple translation
            test_result = self.translate("Hello", "en", "hi")
            
            return {
                "status": "healthy" if test_result["success"] else "degraded",
                "models_loaded": len(self.model_manager.loaded_models),
                "test_translation": test_result["success"],
                "memory_stats": self.model_manager.get_memory_stats()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Global translation engine instance
translation_engine = TranslationEngine()
