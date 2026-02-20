"""
Streamlit Cloud entry point.
This file is required for Streamlit Cloud deployment.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main app (this will execute the Streamlit code)
from ui import app
