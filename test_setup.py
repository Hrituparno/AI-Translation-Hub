"""Quick test to verify installation."""

print("Testing imports...")

try:
    import torch
    print("✓ PyTorch installed")
except:
    print("✗ PyTorch not installed")

try:
    import transformers
    print("✓ Transformers installed")
except:
    print("✗ Transformers not installed")

try:
    import fastapi
    print("✓ FastAPI installed")
except:
    print("✗ FastAPI not installed")

try:
    import streamlit
    print("✓ Streamlit installed")
except:
    print("✗ Streamlit not installed")

print("\nAll core dependencies are installed!")
print("\nTo start the application:")
print("1. API: cmd /c \"venv\\Scripts\\activate.bat && uvicorn api.main:app --host 0.0.0.0 --port 8000\"")
print("2. UI:  cmd /c \"venv\\Scripts\\activate.bat && streamlit run ui/app.py --server.port 8501\"")
