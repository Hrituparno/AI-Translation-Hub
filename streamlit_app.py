"""
Streamlit Cloud entry point.
This file is required for Streamlit Cloud deployment.
"""

# Simply run the UI app
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the app
exec(open("ui/app.py").read())
