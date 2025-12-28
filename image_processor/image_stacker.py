from typing import List, Optional, Dict, Any
from PIL import Image
from UI.ui_manager import UIManager

class ImageStacker:
    def __init__(self, ui_manager: UIManager):
        self.ui_manager = ui_manager()
    
    def run(self):
        self.ui_manager.header()
        self.ui_manager.setup_page()
        settings = self.ui_manager.sidebar()
        uploaded_images = self.ui_manager.file_uploader()
    
    def handle_images(self, images: List[Image.Image], settings: Dict[str, Any]) -> Optional[Image.Image]:
        #get uploaded images from the UI
        uploaded_images = self.ui_manager.file_uploader()
        
        #if no files are uploaded return nothing
        if not uploaded_images:
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
         