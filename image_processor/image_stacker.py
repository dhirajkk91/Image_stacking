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
        
        # Load and validate images
        images = self.ui_manager.display_uploaded_images(uploaded_files)
        if not images:
            self.ui_manager.show_error_message("No valid images could be loaded.")
            return
        
        # Route to appropriate handler
        if len(images) >= 2:
            self._handle_multiple_images(images, settings)
        else:
            self._handle_single_image(images[0], settings)
    
    def _handle_multiple_images(self, images: List[Image.Image], settings: Dict[str, Any]) -> None:
        """
        Optimized multi-image processing with better error handling.
        
        Args:
            images: List of PIL Image objects
            settings: User settings dictionary
        """
        stack_clicked, _ = self.ui_manager.show_processing_buttons(len(images))
        
        if not stack_clicked:
            return
        
        # Process with progress tracking
        with self.ui_manager.show_spinner(f"Stacking {len(images)} images..."):
            enhanced_image = self._process_images_safely(
                lambda: self.image_processor.process_multiple_images(images, settings)
            )
            
            if enhanced_image is None:
                return
            
            # Get export info and display results
            export_info = self.image_processor.get_export_info(enhanced_image, settings)
            self.ui_manager.display_processing_results(enhanced_image, export_info)
            self._handle_image_download(enhanced_image, settings)
            self.ui_manager.show_success_message("Image stacking complete!")
    
    def _handle_single_image(self, image: Image.Image, settings: Dict[str, Any]) -> None:
        """
        Optimized single image processing.
        
        Args:
            image: PIL Image object
            settings: User settings dictionary
        """
        _, upscale_clicked = self.ui_manager.show_processing_buttons(1)
        
        if not upscale_clicked:
            return
        
        # Process with progress tracking
        with self.ui_manager.show_spinner("Enhancing image..."):
            enhanced_image = self._process_images_safely(
                lambda: self.image_processor.process_single_image(image, settings)
            )
            
            if enhanced_image is None:
                return
            
            # Get export info and display results
            export_info = self.image_processor.get_export_info(enhanced_image, settings)
            self.ui_manager.display_processing_results(enhanced_image, export_info)
            self._handle_image_download(enhanced_image, settings)
            self.ui_manager.show_success_message("Image enhancement complete!")
    
    def _process_images_safely(self, process_func) -> Optional[Image.Image]:
        """
        Safe image processing with comprehensive error handling.
        
        Args:
            process_func: Function to execute for processing
            
        Returns:
            Processed image or None if failed
        """
        try:
            result = process_func()
            if result is None:
                self.ui_manager.show_error_message("Processing failed - please try again")
            return result
            
        except MemoryError:
            self.ui_manager.show_error_message(
                "Not enough memory. Try reducing upscale factor or image count."
            )
        except ValueError as e:
            self.ui_manager.show_error_message(f"Invalid input: {str(e)}")
        except Exception as e:
            self.ui_manager.show_error_message(f"Processing error: {str(e)}")
        
        return None
    
    def _handle_image_download(self, image: Image.Image, settings: Dict[str, Any]) -> None:
        """
        Optimized image export and download with error handling.
        
        Args:
            image: PIL Image object to export
            settings: User settings dictionary
        """
        try:
            # Export image
            image_data, filename = self.image_processor.export_processed_image(image, settings)
            
            # Create download button
            self.ui_manager.create_download_button(image_data, filename)
            
        except Exception as e:
            self.ui_manager.show_error_message(f"Export failed: {str(e)}")


def main() -> None:
    """Optimized application entry point."""
    try:
        app = ImageStackerApp()
        app.run()
    except Exception as e:
        import streamlit as st
        st.error(f"Application startup failed: {str(e)}")
        st.info("Try refreshing the page or check your installation")


if __name__ == "__main__":
    main()