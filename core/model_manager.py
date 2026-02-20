"""
Dynamic model manager with lazy loading and memory optimization.
Handles loading, caching, and unloading of translation models.
Supports both NLLB (Google Translate quality) and MarianMT (lightweight) models.
"""

import gc
import torch
from transformers import (
    MarianMTModel, 
    MarianTokenizer,
    AutoModelForSeq2SeqLM,
    AutoTokenizer
)
from functools import lru_cache
from typing import Tuple, Optional
import logging

from core.config import (
    MODEL_MAPPINGS,
    MAX_MODELS_IN_MEMORY,
    MAX_INPUT_LENGTH,
    ENABLE_QUANTIZATION,
    USE_NLLB_MODEL,
    NLLB_MODEL_NAME,
    NLLB_LANG_CODES,
    NUM_BEAMS,
    LENGTH_PENALTY,
    NO_REPEAT_NGRAM_SIZE,
    EARLY_STOPPING
)

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages translation models with memory-efficient loading and caching."""
    
    def __init__(self):
        self.loaded_models = {}  # {model_name: (model, tokenizer)}
        self.load_order = []  # Track loading order for LRU eviction
        self.device = "cpu"  # Force CPU for low-memory environments
        self.use_nllb = USE_NLLB_MODEL  # Use NLLB for better quality
        self.nllb_model = None
        self.nllb_tokenizer = None
        
    def get_model_name(self, source_lang: str, target_lang: str) -> Optional[str]:
        """Get the model name for a language pair."""
        pair = (source_lang, target_lang)
        return MODEL_MAPPINGS.get(pair)
    
    def _load_nllb_model(self):
        """Load the NLLB model for high-quality translation."""
        if self.nllb_model is not None:
            return self.nllb_model, self.nllb_tokenizer
        
        logger.info(f"Loading NLLB model: {NLLB_MODEL_NAME}")
        
        try:
            # Load tokenizer
            self.nllb_tokenizer = AutoTokenizer.from_pretrained(
                NLLB_MODEL_NAME,
                model_max_length=MAX_INPUT_LENGTH
            )
            
            # Load model with memory optimization
            self.nllb_model = AutoModelForSeq2SeqLM.from_pretrained(
                NLLB_MODEL_NAME,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
            
            # Move to CPU and set to eval mode
            self.nllb_model = self.nllb_model.to(self.device)
            self.nllb_model.eval()
            
            # Apply quantization for memory efficiency
            if ENABLE_QUANTIZATION:
                try:
                    self.nllb_model = torch.quantization.quantize_dynamic(
                        self.nllb_model, {torch.nn.Linear}, dtype=torch.qint8
                    )
                    logger.info("Applied 8-bit quantization to NLLB model")
                except Exception as e:
                    logger.warning(f"Quantization failed: {e}")
            
            logger.info("Successfully loaded NLLB model")
            return self.nllb_model, self.nllb_tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load NLLB model: {e}")
            logger.info("Falling back to MarianMT models")
            self.use_nllb = False
            raise
    
    def _evict_oldest_model(self):
        """Remove the least recently used model to free memory."""
        if len(self.loaded_models) >= MAX_MODELS_IN_MEMORY and self.load_order:
            oldest_model = self.load_order.pop(0)
            if oldest_model in self.loaded_models:
                logger.info(f"Evicting model from memory: {oldest_model}")
                del self.loaded_models[oldest_model]
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
    
    def load_model(self, model_name: str) -> Tuple[MarianMTModel, MarianTokenizer]:
        """
        Load a translation model with memory optimization.
        
        Args:
            model_name: HuggingFace model identifier
            
        Returns:
            Tuple of (model, tokenizer)
        """
        # Check if already loaded
        if model_name in self.loaded_models:
            logger.info(f"Using cached model: {model_name}")
            # Update LRU order
            if model_name in self.load_order:
                self.load_order.remove(model_name)
            self.load_order.append(model_name)
            return self.loaded_models[model_name]
        
        # Evict old models if necessary
        self._evict_oldest_model()
        
        logger.info(f"Loading model: {model_name}")
        
        try:
            # Load tokenizer
            tokenizer = MarianTokenizer.from_pretrained(
                model_name,
                model_max_length=MAX_INPUT_LENGTH
            )
            
            # Load model with memory optimization
            model = MarianMTModel.from_pretrained(
                model_name,
                torch_dtype=torch.float32,  # Use float32 for CPU
                low_cpu_mem_usage=True  # Optimize memory during loading
            )
            
            # Move to CPU and set to eval mode
            model = model.to(self.device)
            model.eval()
            
            # Optional: Apply quantization for further memory reduction
            if ENABLE_QUANTIZATION:
                try:
                    model = torch.quantization.quantize_dynamic(
                        model, {torch.nn.Linear}, dtype=torch.qint8
                    )
                    logger.info(f"Applied quantization to {model_name}")
                except Exception as e:
                    logger.warning(f"Quantization failed: {e}")
            
            # Cache the model
            self.loaded_models[model_name] = (model, tokenizer)
            self.load_order.append(model_name)
            
            logger.info(f"Successfully loaded model: {model_name}")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise
    
    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """
        Translate text using the appropriate model.
        Uses NLLB for better quality (Google Translate-like) or MarianMT as fallback.
        
        Args:
            text: Input text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text or None if model not available
        """
        # Try NLLB first if enabled
        if self.use_nllb:
            try:
                return self._translate_with_nllb(text, source_lang, target_lang)
            except Exception as e:
                logger.error(f"NLLB translation failed: {e}")
                logger.info("Falling back to MarianMT")
                self.use_nllb = False
        
        # Fallback to MarianMT
        return self._translate_with_marian(text, source_lang, target_lang)
    
    def _translate_with_nllb(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """Translate using NLLB model (high quality)."""
        try:
            model, tokenizer = self._load_nllb_model()
            
            # Convert language codes to NLLB format
            src_lang_code = NLLB_LANG_CODES.get(source_lang)
            tgt_lang_code = NLLB_LANG_CODES.get(target_lang)
            
            if not src_lang_code or not tgt_lang_code:
                logger.warning(f"Language not supported by NLLB: {source_lang} or {target_lang}")
                return None
            
            # Set source language
            tokenizer.src_lang = src_lang_code
            
            # Tokenize input
            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=MAX_INPUT_LENGTH
            ).to(self.device)
            
            # Generate translation with improved parameters
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang_code],
                    max_length=MAX_INPUT_LENGTH,
                    num_beams=NUM_BEAMS,
                    length_penalty=LENGTH_PENALTY,
                    no_repeat_ngram_size=NO_REPEAT_NGRAM_SIZE,
                    early_stopping=EARLY_STOPPING
                )
            
            # Decode output
            translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return translated
            
        except Exception as e:
            logger.error(f"NLLB translation failed: {e}")
            raise
    
    def _translate_with_marian(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """Translate using MarianMT model (lightweight fallback)."""
        model_name = self.get_model_name(source_lang, target_lang)
        
        if not model_name:
            logger.warning(f"No model found for {source_lang} -> {target_lang}")
            return None
        
        try:
            model, tokenizer = self.load_model(model_name)
            
            # Tokenize input
            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=MAX_INPUT_LENGTH
            ).to(self.device)
            
            # Generate translation with improved parameters
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_length=MAX_INPUT_LENGTH,
                    num_beams=NUM_BEAMS,
                    length_penalty=LENGTH_PENALTY,
                    no_repeat_ngram_size=NO_REPEAT_NGRAM_SIZE,
                    early_stopping=EARLY_STOPPING
                )
            
            # Decode output
            translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return translated
            
        except Exception as e:
            logger.error(f"MarianMT translation failed: {e}")
            return None
    
    def unload_all_models(self):
        """Unload all models to free memory."""
        logger.info("Unloading all models")
        self.loaded_models.clear()
        self.load_order.clear()
        self.nllb_model = None
        self.nllb_tokenizer = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def get_memory_stats(self) -> dict:
        """Get current memory usage statistics."""
        return {
            "loaded_models": len(self.loaded_models),
            "model_names": list(self.loaded_models.keys()),
            "max_models": MAX_MODELS_IN_MEMORY
        }


# Global model manager instance
model_manager = ModelManager()
