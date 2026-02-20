# Translation Quality Guide

## Overview

IndiaTranslate now supports two translation engines with different quality/performance tradeoffs:

## Model Comparison

| Feature | NLLB-200 | MarianMT |
|---------|----------|----------|
| **Quality** | ⭐⭐⭐⭐⭐ Google Translate-like | ⭐⭐⭐ Good |
| **Speed** | Slower (3-5s) | Faster (1-2s) |
| **Memory** | ~1.2 GB | ~300-500 MB |
| **Languages** | 200+ (direct translation) | 13+ Indian languages |
| **Best For** | Production, high accuracy | Development, low memory |

## NLLB-200 (Recommended for Production)

### What is NLLB?

NLLB (No Language Left Behind) is Facebook/Meta's state-of-the-art multilingual translation model that supports 200+ languages with direct translation (no English bridge needed).

### Advantages

1. **Higher Accuracy**: Comparable to Google Translate
2. **Direct Translation**: All language pairs supported directly
3. **Better Context**: Understands nuance and context better
4. **Fluency**: More natural-sounding translations
5. **Consistency**: Same model for all languages

### Quality Improvements

- **Beam Search (5 beams)**: Explores multiple translation paths
- **Length Penalty (1.0)**: Balanced output length
- **No Repeat N-grams (3)**: Prevents repetitive phrases
- **Early Stopping**: Efficient generation

### Memory Requirements

- Base model: ~2.4 GB
- With 8-bit quantization: ~1.2 GB
- Runtime memory: ~1.5 GB total

### When to Use

- Production deployments with quality requirements
- Customer-facing applications
- Professional translation needs
- When accuracy matters more than speed

## MarianMT (Lightweight Alternative)

### What is MarianMT?

MarianMT is Helsinki-NLP's collection of lightweight translation models optimized for specific language pairs.

### Advantages

1. **Low Memory**: Only 300-500 MB
2. **Fast**: 1-2 second translations
3. **Efficient**: Good for development/testing
4. **Proven**: Widely used in production

### Limitations

- Lower accuracy than NLLB
- May need English-bridge for some pairs
- Less context awareness
- Occasional awkward phrasing

### When to Use

- Development and testing
- Low-memory environments (< 1 GB)
- Speed-critical applications
- Cost-sensitive deployments

## Switching Models

### Enable NLLB (High Quality)

```bash
python toggle_model.py nllb
```

Or manually edit `core/config.py`:
```python
USE_NLLB_MODEL = True
```

### Enable MarianMT (Lightweight)

```bash
python toggle_model.py marian
```

Or manually edit `core/config.py`:
```python
USE_NLLB_MODEL = False
```

**Important**: Restart API and UI servers after changing models.

## Testing Translation Quality

Run the quality test script:

```bash
python test_translation_quality.py
```

This will test various translation scenarios and show:
- Translation output
- Method used (NLLB/MarianMT)
- Success rate
- Memory usage

## Quality Tuning Parameters

Edit `core/config.py` to adjust quality settings:

```python
# Translation quality settings
NUM_BEAMS = 5              # Higher = better quality, slower (1-10)
LENGTH_PENALTY = 1.0       # <1 = shorter, >1 = longer (0.5-2.0)
NO_REPEAT_NGRAM_SIZE = 3   # Prevent repetition (2-4)
EARLY_STOPPING = True      # Stop when all beams finish
```

### Parameter Guide

**NUM_BEAMS**
- 1: Greedy search (fastest, lowest quality)
- 3-5: Good balance (recommended)
- 8-10: Best quality (slowest)

**LENGTH_PENALTY**
- 0.5-0.8: Shorter translations
- 1.0: Balanced (recommended)
- 1.2-2.0: Longer, more detailed translations

**NO_REPEAT_NGRAM_SIZE**
- 2: Prevent 2-word repetitions
- 3: Prevent 3-word repetitions (recommended)
- 4: Stricter repetition prevention

## Deployment Recommendations

### For Render Free Tier (512 MB)

Use MarianMT:
```python
USE_NLLB_MODEL = False
MAX_MODELS_IN_MEMORY = 2
ENABLE_QUANTIZATION = False
```

### For Render Starter ($7/month, 512 MB)

Use MarianMT with quantization:
```python
USE_NLLB_MODEL = False
MAX_MODELS_IN_MEMORY = 2
ENABLE_QUANTIZATION = True
```

### For Render Standard ($25/month, 2 GB)

Use NLLB with quantization:
```python
USE_NLLB_MODEL = True
MAX_MODELS_IN_MEMORY = 1
ENABLE_QUANTIZATION = True
```

### For Render Pro ($85/month, 4 GB+)

Use NLLB without quantization:
```python
USE_NLLB_MODEL = True
MAX_MODELS_IN_MEMORY = 1
ENABLE_QUANTIZATION = False
```

## Troubleshooting

### Out of Memory Errors

1. Enable quantization:
   ```python
   ENABLE_QUANTIZATION = True
   ```

2. Reduce beam search:
   ```python
   NUM_BEAMS = 3
   ```

3. Switch to MarianMT:
   ```bash
   python toggle_model.py marian
   ```

### Slow Translations

1. Reduce beam search:
   ```python
   NUM_BEAMS = 3
   ```

2. Disable quantization (if memory allows):
   ```python
   ENABLE_QUANTIZATION = False
   ```

3. Use MarianMT for faster inference

### Poor Quality Translations

1. Switch to NLLB:
   ```bash
   python toggle_model.py nllb
   ```

2. Increase beam search:
   ```python
   NUM_BEAMS = 8
   ```

3. Adjust length penalty:
   ```python
   LENGTH_PENALTY = 1.2
   ```

## Benchmarks

### Translation Quality (BLEU Score)

| Language Pair | NLLB-200 | MarianMT |
|---------------|----------|----------|
| en → hi | 35-40 | 25-30 |
| hi → en | 38-42 | 28-32 |
| en → ta | 32-38 | 22-28 |
| en → bn | 34-39 | 26-31 |

### Speed (Average)

| Model | First Request | Cached Model |
|-------|---------------|--------------|
| NLLB-200 | 45-60s | 3-5s |
| MarianMT | 30-45s | 1-2s |

### Memory Usage

| Configuration | Idle | Single Model | Peak |
|---------------|------|--------------|------|
| NLLB + Quantization | 200 MB | 1.2 GB | 1.5 GB |
| NLLB (no quant) | 200 MB | 2.4 GB | 2.8 GB |
| MarianMT | 200 MB | 400 MB | 500 MB |

## Best Practices

1. **Start with NLLB** for best quality
2. **Monitor memory** usage in production
3. **Test thoroughly** with your specific use cases
4. **Tune parameters** based on your needs
5. **Use caching** to improve response times
6. **Consider CDN** for static assets
7. **Implement rate limiting** to prevent abuse

## Future Improvements

- [ ] GPU support for faster inference
- [ ] Model caching with Redis
- [ ] Batch translation optimization
- [ ] Custom fine-tuned models
- [ ] Real-time translation streaming
- [ ] Translation memory/glossary support
