"""
Optimized main application coordinator with enhanced error handling and performance.
"""
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from PIL import Image
from image_processor.image_processing import ImageProcessor
from UI.ui_manager import UIManager


class ImageStackerApp:
    """High-performance application coordinator with optimized workflow."""
    
    __slots__ = ('ui_manager', 'image_processor')
    
    def __init__(self):
        self.ui_manager = UIManager()
        self.image_processor = ImageProcessor()
    
    def run(self) -> None:
        """Optimized application entry point."""
        # Setup page (cached)
        self.ui_manager.setup_page_config()
        self.ui_manager.display_header()
        
        # Get settings and handle uploads
        settings = self.ui_manager.create_settings_sidebar()
        self._handle_file_uploads(settings)
    
    def _handle_file_uploads(self, settings: Dict[str, Any]) -> None:
        """
        Optimized file upload handling with early returns.
        
        Args:
            settings: Dictionary containing user settings from sidebar
        """
        uploaded_files = self.ui_manager.create_file_uploader()
        
        if not uploaded_files:
            self.ui_manager.show_instructions()
            return
        
        # load images using PIL
        images = self.ui_manager.display_uploaded_images(uploaded_images)
        
        if not images:
            return
        
        # routing the image to it handler
        if len(images) >=2:
            self._handle_multiple_images(images, settings)
        else:
            self._handle_single_image(images[0], settings)
            
    def _handle_single_image(self, image: Image.Image, settings: Dict[str, Any]) -> Image.Image:
        
         _, upscale_clicked = self.ui_manager.show_processing_buttons(1)
         if not upscale_clicked:
             return image
         