import streamlit as st
from PIL import Image
from typing import List, Tuple, Optional, Dict, Any
import io
from functools import lru_cache

class UIManager:
    
    SUPPORTED_TYPES = ('png', 'jpg', 'jpeg', 'tiff')
    OUTPUT_FORMATS = ("PNG", "JPEG", "TIFF")
    
    def setup_page(self):
        """
        this method sets up the Streamlit page configuration. 
        It defines the page title, icon, layout, and initial sidebar state.
        """
        st.set_page_config(
            page_title="Image Stacking App",
            page_icon="🌆",
            layout="centered",
            initial_sidebar_state="auto"
        )
    def header(self):
        """
        This method creates the header section of the Streamlit app.
        """
        st.title("📸 Image Stacking Application 📸")
        st.markdown("*Upload your images to stack them*")
        
    def sidebar(self) -> Dict[str, Any]:
        """
        Optimized settings sidebar with better UX.
        
        Returns:
            Dictionary containing user settings
        """
        with st.sidebar:
            st.header("⚙️ Settings")
            
            # Upscale factor with better UX
            upscale_factor = st.slider(
                "🔍 Upscale Factor", 
                min_value=1.0, 
                max_value=4.0, 
                value=2.0, 
                step=0.25,
                help="Higher values increase resolution but take more time"
            )
            
            # Output format selection
            output_format = st.selectbox(
                "📁 Output Format", 
                self.OUTPUT_FORMATS,
                help="PNG: Lossless, larger files | JPEG: Smaller files | TIFF: Professional"
            )
            
            # Conditional JPEG quality
            jpeg_quality = None
            if output_format == "JPEG":
                jpeg_quality = st.slider(
                    "🎯 JPEG Quality", 
                    min_value=60, 
                    max_value=100, 
                    value=95,
                    help="Higher quality = larger file size"
                )

        return {
            'upscale_factor': upscale_factor,
            'output_format': output_format,
            'jpeg_quality': jpeg_quality
        }
    
    def file_uploader(self):
        """
        This method creates a file uploader in the Streamlit app.
        """
        uploaded_files = st.file_uploader(
            "Choose images to upload",
            type=self.SUPPORTED_TYPES,
            accept_multiple_files=True
        )
        return uploaded_files or []
    
    # button_text, data, file_name are kept random to check the UI later need to fix this
    def download_button(self, button_text="Download File", data=None, file_name="output.png"):
        """
        This method creates a download button in the Streamlit app.
        """
        # Use test data if no data is provided
        if data is None:
            data = b"Test data for download button"
        
        st.download_button(
            label=button_text,
            data=data,
            file_name=file_name,
            mime="image/png"
        )