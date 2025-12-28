"""
Image Stacker & Quality Enhancer - Streamlit App

High-performance image processing application with modular architecture.
"""

import sys
from pathlib import Path
import streamlit as st

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from image_processor.image_stacker import ImageStackerApp
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please install dependencies: pip install -r requirements.txt")
    st.stop()

# Initialize and run the app
try:
    app = ImageStackerApp()
    app.run()
except Exception as e:
    st.error(f"Application error: {e}")
    st.info("Please check your installation and try refreshing the page.")