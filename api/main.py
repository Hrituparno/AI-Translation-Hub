"""
FastAPI backend for translation service.
Production-ready REST API with rate limiting and error handling.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import time
import logging
from collections import defaultdict

from core.translator import translation_engine
from core.config import SUPPORTED_LANGUAGES, LANGUAGE_NAMES, API_RATE_LIMIT
from utils.memory import get_memory_usage, log_memory_usage
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="IndiaTranslate API",
    description="Production AI Translation API for Indian Languages",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple rate limiting (in-memory)
rate_limit_store = defaultdict(list)


# Request/Response models
class TranslationRequest(BaseModel):
    text: str = Field(..., description="Text to translate", min_length=1, max_length=5000)
    source_lang: Optional[str] = Field(None, description="Source language code (auto-detect if None)")
    target_lang: str = Field("en", description="Target language code")
    auto_detect: bool = Field(True, description="Enable automatic language detection")


class TranslationResponse(BaseModel):
    success: bool
    translated_text: Optional[str]
    source_lang: str
    target_lang: str
    method: Optional[str]
    error: Optional[str] = None


class BatchTranslationRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to translate", max_items=50)
    source_lang: Optional[str] = None
    target_lang: str = "en"


class HealthResponse(BaseModel):
    status: str
    models_loaded: int
    memory_usage_mb: float
    supported_languages: int


# Middleware for rate limiting
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple rate limiting middleware."""
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old entries
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip]
        if current_time - t < 60
    ]
    
    # Check rate limit
    if len(rate_limit_store[client_ip]) >= API_RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Please try again later."}
        )
    
    rate_limit_store[client_ip].append(current_time)
    response = await call_next(request)
    return response


# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "IndiaTranslate API",
        "version": "1.0.0",
        "description": "AI-powered translation for Indian languages",
        "endpoints": {
            "translate": "/translate",
            "batch": "/batch-translate",
            "languages": "/languages",
            "health": "/health"
        }
    }


@app.post("/translate", response_model=TranslationResponse, tags=["Translation"])
async def translate(request: TranslationRequest):
    """
    Translate text between languages.
    
    - Supports auto-detection of source language
    - Falls back to English-bridge for unsupported pairs
    - Returns translation metadata
    """
    try:
        log_memory_usage("[API] Before translation")
        
        result = translation_engine.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            auto_detect=request.auto_detect
        )
        
        log_memory_usage("[API] After translation")
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Translation failed"))
        
        return TranslationResponse(**result)
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-translate", tags=["Translation"])
async def batch_translate(request: BatchTranslationRequest):
    """
    Translate multiple texts in a single request.
    
    - Maximum 50 texts per request
    - Returns array of translation results
    """
    try:
        if len(request.texts) > 50:
            raise HTTPException(status_code=400, detail="Maximum 50 texts per batch")
        
        results = translation_engine.batch_translate(
            texts=request.texts,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return {"results": results, "count": len(results)}
        
    except Exception as e:
        logger.error(f"Batch translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/languages", tags=["Information"])
async def get_languages():
    """Get list of supported languages."""
    languages = [
        {
            "code": code,
            "name": LANGUAGE_NAMES.get(code, code.upper())
        }
        for code in SUPPORTED_LANGUAGES
    ]
    
    return {
        "languages": languages,
        "count": len(languages)
    }


@app.get("/translation-pairs", tags=["Information"])
async def get_translation_pairs():
    """Get list of supported translation pairs."""
    pairs = translation_engine.get_supported_pairs()
    return {
        "pairs": pairs,
        "count": len(pairs)
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    
    - Returns system status
    - Memory usage statistics
    - Model loading status
    """
    try:
        health = translation_engine.health_check()
        memory = get_memory_usage()
        
        return HealthResponse(
            status=health["status"],
            models_loaded=health["models_loaded"],
            memory_usage_mb=round(memory["rss_mb"], 2),
            supported_languages=len(SUPPORTED_LANGUAGES)
        )
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            models_loaded=0,
            memory_usage_mb=0,
            supported_languages=0
        )


@app.get("/memory", tags=["Monitoring"])
async def get_memory_stats():
    """Get detailed memory statistics."""
    memory = get_memory_usage()
    model_stats = translation_engine.model_manager.get_memory_stats()
    
    return {
        "memory": memory,
        "models": model_stats
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Starting IndiaTranslate API")
    log_memory_usage("[STARTUP]")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down IndiaTranslate API")
    translation_engine.model_manager.unload_all_models()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
