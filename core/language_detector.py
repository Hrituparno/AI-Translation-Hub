"""
Lightweight language detection for Indian languages.
Uses langdetect with fallback mechanisms.
"""

import logging
from typing import Optional
import re

try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0  # For consistent results
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

from core.config import SUPPORTED_LANGUAGES, LANGUAGE_CODES

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detect source language with support for Indian languages."""
    
    def __init__(self):
        self.supported_langs = set(SUPPORTED_LANGUAGES)
        
        # Script-based detection patterns for Indian languages
        self.script_patterns = {
            "hi": re.compile(r'[\u0900-\u097F]'),  # Devanagari (Hindi, Marathi, Sanskrit)
            "bn": re.compile(r'[\u0980-\u09FF]'),  # Bengali
            "ta": re.compile(r'[\u0B80-\u0BFF]'),  # Tamil
            "te": re.compile(r'[\u0C00-\u0C7F]'),  # Telugu
            "gu": re.compile(r'[\u0A80-\u0AFF]'),  # Gujarati
            "kn": re.compile(r'[\u0C80-\u0CFF]'),  # Kannada
            "ml": re.compile(r'[\u0D00-\u0D7F]'),  # Malayalam
            "pa": re.compile(r'[\u0A00-\u0A7F]'),  # Punjabi (Gurmukhi)
            "or": re.compile(r'[\u0B00-\u0B7F]'),  # Odia
            "as": re.compile(r'[\u0980-\u09FF]'),  # Assamese (similar to Bengali)
        }
        
        # Urdu uses Arabic script
        self.script_patterns["ur"] = re.compile(r'[\u0600-\u06FF]')
    
    def detect_by_script(self, text: str) -> Optional[str]:
        """
        Detect language based on Unicode script ranges.
        More reliable for Indian languages than langdetect.
        """
        # Count characters matching each script
        script_scores = {}
        
        for lang, pattern in self.script_patterns.items():
            matches = len(pattern.findall(text))
            if matches > 0:
                script_scores[lang] = matches
        
        if script_scores:
            # Return language with most matching characters
            detected = max(script_scores, key=script_scores.get)
            logger.info(f"Script-based detection: {detected}")
            return detected
        
        return None
    
    def detect_by_langdetect(self, text: str) -> Optional[str]:
        """Detect language using langdetect library."""
        if not LANGDETECT_AVAILABLE:
            return None
        
        try:
            detected = detect(text)
            
            # Map langdetect codes to our codes
            lang_map = {
                "hi": "hi",
                "bn": "bn",
                "ta": "ta",
                "te": "te",
                "mr": "mr",
                "gu": "gu",
                "kn": "kn",
                "ml": "ml",
                "pa": "pa",
                "ur": "ur",
                "or": "or",
                "en": "en"
            }
            
            mapped = lang_map.get(detected)
            if mapped and mapped in self.supported_langs:
                logger.info(f"Langdetect detection: {mapped}")
                return mapped
                
        except Exception as e:
            logger.warning(f"Langdetect failed: {e}")
        
        return None
    
    def detect_hinglish(self, text: str) -> bool:
        """
        Detect if text is Hinglish (Hindi-English mix).
        Returns True if text contains both Latin and Devanagari scripts.
        """
        has_latin = bool(re.search(r'[a-zA-Z]', text))
        has_devanagari = bool(self.script_patterns["hi"].search(text))
        
        return has_latin and has_devanagari
    
    def detect(self, text: str, default: str = "en") -> str:
        """
        Detect language with multiple fallback strategies.
        
        Args:
            text: Input text to detect
            default: Default language if detection fails
            
        Returns:
            Detected language code
        """
        if not text or not text.strip():
            return default
        
        # Check for Hinglish
        if self.detect_hinglish(text):
            logger.info("Detected Hinglish - treating as Hindi")
            return "hi"
        
        # Try script-based detection first (more reliable for Indian languages)
        script_lang = self.detect_by_script(text)
        if script_lang:
            return script_lang
        
        # Fallback to langdetect
        langdetect_lang = self.detect_by_langdetect(text)
        if langdetect_lang:
            return langdetect_lang
        
        # Check if text is primarily English (Latin script)
        if re.search(r'[a-zA-Z]', text):
            logger.info("Detected Latin script - defaulting to English")
            return "en"
        
        logger.warning(f"Could not detect language, using default: {default}")
        return default
    
    def get_language_info(self, text: str) -> dict:
        """Get detailed language detection information."""
        detected = self.detect(text)
        is_hinglish = self.detect_hinglish(text)
        
        return {
            "detected_language": detected,
            "is_hinglish": is_hinglish,
            "confidence": "high" if self.detect_by_script(text) else "medium"
        }


# Global detector instance
language_detector = LanguageDetector()
