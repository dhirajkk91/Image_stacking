import streamlit as st
from PIL import Image
from typing import List, Tuple, Optional, Dict, Any
import io
from functools import lru_cache

class UIManager:
    
    SUPPORTED_TYPES = ('png', 'jpg', 'jpeg', 'tiff')
    OUTPUT_FORMATS = ("PNG", "JPEG", "TIFF")
    
    def setup_page_config(self):
        """
        Alias for setup_page method for compatibility.
        """
        return self.setup_page()
    
    def display_header(self):
        """
        Alias for header method for compatibility.
        """
        return self.header()
    
    def create_settings_sidebar(self) -> Dict[str, Any]:
        """
        Alias for sidebar method for compatibility.
        """
        return self.sidebar()
    
    def create_file_uploader(self):
        """
        Alias for file_uploader method for compatibility.
        """
        return self.file_uploader()
    
    def show_instructions(self):
        """
        Display instructions when no files are uploaded.
        """
        st.info("Please upload 2 or more images to start stacking, or upload 1 image for enhancement.")
    
    
    def display_uploaded_images(self, uploaded_files) -> List[Image.Image]:
        """
        Display uploaded images and return PIL Image objects.
        
        Args:
            uploaded_files: List of uploaded file objects
            
        Returns:
            List of PIL Image objects
        """
        if not uploaded_files:
            return []
        
        st.subheader(f"📁 Uploaded Images ({len(uploaded_files)})")
        
        images = []
        cols = st.columns(min(len(uploaded_files), 3))
        
        for idx, uploaded_file in enumerate(uploaded_files):
            try:
                # Load image
                image = Image.open(uploaded_file)
                images.append(image)
                
                # Display in column
                with cols[idx % 3]:
                    st.image(image, caption=uploaded_file.name, use_column_width=True)
                    st.caption(f"Size: {image.width}x{image.height}")
                    
            except Exception as e:
                st.error(f"Error loading {uploaded_file.name}: {str(e)}")
        
        return images
    
    def show_error_message(self, message: str):
        """
        Display an error message.
        
        Args:
            message: Error message to display
        """
        st.error(f"{message}")
    
    def show_processing_buttons(self, num_images: int) -> Tuple[bool, bool]:
        """
        Show processing buttons based on number of images.
        
        Args:
            num_images: Number of uploaded images
            
        Returns:
            Tuple of (stack_clicked, enhance_clicked)
        """
        st.subheader("Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if num_images >= 2:
                stack_clicked = st.button(
                    f"📚 Stack {num_images} Images",
                    help="Combine multiple images for noise reduction and enhanced quality",
                    use_container_width=True
                )
            else:
                stack_clicked = False
                st.button(
                    "📚 Stack Images",
                    disabled=True,
                    help="Need 2+ images for stacking",
                    use_container_width=True
                )
        
        with col2:
            enhance_clicked = st.button(
                "✨ Enhance Single Image",
                help="Upscale and enhance the first uploaded image",
                use_container_width=True
            )
        
        return stack_clicked, enhance_clicked
    
    def show_spinner(self, text: str):
        """
        Show a spinner with custom text.
        
        Args:
            text: Text to display with spinner
            
        Returns:
            Streamlit spinner context manager
        """
        return st.spinner(text)
    
    def display_processing_results(self, image: Image.Image, export_info: Dict[str, Any]):
        """
        Display processing results and image information.
        
        Args:
            image: Processed PIL Image
            export_info: Dictionary with export information
        """
        st.subheader("Processing Complete!")

        # Display result image
        st.image(image, caption="Processed Image", use_column_width=True)
        
        # Display image info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dimensions", export_info.get('dimensions', 'Unknown'))
        with col2:
            st.metric("Format", export_info.get('format', 'Unknown'))
        with col3:
            st.metric("Est. Size", export_info.get('size_estimate', 'Unknown'))
    
    def create_download_button(self, image_data: bytes, filename: str) -> bool:
        """
        Create a download button for processed image.
        
        Args:
            image_data: Processed image as bytes
            filename: Filename for download
            
        Returns:
            True if button was clicked
        """
        return st.download_button(
            label="Download Processed Image",
            data=image_data,
            file_name=filename,
            mime="image/png" if filename.endswith('.png') else "image/jpeg",
            use_container_width=True
        )
    
    def show_success_message(self, message: str):
        """
        Display a success message.
        
        Args:
            message: Success message to display
        """
        st.success(f"{message}")

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
                "Upscale Factor", 
                min_value=1.0, 
                max_value=4.0, 
                value=2.0, 
                step=0.25,
                help="Higher values increase resolution but take more time"
            )
            
            # Output format selection
            output_format = st.selectbox(
                "Output Format", 
                self.OUTPUT_FORMATS,
                help="PNG: Lossless, larger files | JPEG: Smaller files | TIFF: Professional"
            )
            
            # Conditional JPEG quality
            jpeg_quality = None
            if output_format == "JPEG":
                jpeg_quality = st.slider(
                    "JPEG Quality", 
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
    
    def download_button(self, button_text="Download File", data=None, file_name="output.png"):
        """
        This method creates a download button in the Streamlit app.
        """
        # Use actual data if provided, otherwise show placeholder
        if data is None:
            st.info("Process an image to enable download")
            return
        
        # Determine MIME type based on file extension
        if file_name.lower().endswith('.jpg') or file_name.lower().endswith('.jpeg'):
            mime_type = "image/jpeg"
        elif file_name.lower().endswith('.png'):
            mime_type = "image/png"
        elif file_name.lower().endswith('.tiff') or file_name.lower().endswith('.tif'):
            mime_type = "image/tiff"
        else:
            mime_type = "application/octet-stream"
        
        st.download_button(
            label=button_text,
            data=data,
            file_name=file_name,
            mime=mime_type
        )