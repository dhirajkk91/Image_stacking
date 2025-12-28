import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import List, Dict, Any, Tuple, Optional


class ImageProcessor:
    """
    High-performance image processing class for stacking and enhancement.
    """
    
    def __init__(self):
        """Initialize the image processor."""
        pass
    
    def process_multiple_images(self, images: List[Image.Image], settings: Dict[str, Any]) -> Image.Image:
        """
        Stack multiple images using advanced alignment and blending.
        
        Args:
            images: List of PIL Image objects to stack
            settings: Processing settings including upscale_factor
            
        Returns:
            Stacked and enhanced PIL Image
        """
        if len(images) < 2:
            raise ValueError("Need at least 2 images for stacking")
        
        # Convert to numpy arrays for processing
        np_images = [np.array(img) for img in images]
        
        # Align images (simple implementation)
        aligned_images = self._align_images(np_images)
        
        # Stack using median blending for noise reduction
        stacked = np.median(aligned_images, axis=0).astype(np.uint8)
        
        # Convert back to PIL and enhance
        result = Image.fromarray(stacked)
        
        # Apply upscaling if requested
        upscale_factor = settings.get('upscale_factor', 1.0)
        if upscale_factor > 1.0:
            result = self._upscale_image(result, upscale_factor)
        
        # Apply enhancement
        result = self._enhance_image(result)
        
        return result
    
    def process_single_image(self, image: Image.Image, settings: Dict[str, Any]) -> Image.Image:
        """
        Process a single image with enhancement and upscaling.
        
        Args:
            image: PIL Image to process
            settings: Processing settings
            
        Returns:
            Enhanced PIL Image
        """
        result = image.copy()
        
        # Apply upscaling if requested
        upscale_factor = settings.get('upscale_factor', 1.0)
        if upscale_factor > 1.0:
            result = self._upscale_image(result, upscale_factor)
        
        # Apply enhancement
        result = self._enhance_image(result)
        
        return result
    
    def export_processed_image(self, image: Image.Image, settings: Dict[str, Any]) -> Tuple[bytes, str]:
        """
        Export processed image to specified format.
        
        Args:
            image: PIL Image to export
            settings: Export settings including format and quality
            
        Returns:
            Tuple of (image_bytes, filename)
        """
        import io
        
        output_format = settings.get('output_format', 'PNG')
        jpeg_quality = settings.get('jpeg_quality', 95)
        
        # Generate filename
        filename = f"processed_image.{output_format.lower()}"
        
        # Export to bytes
        buffer = io.BytesIO()
        if output_format == 'JPEG':
            image.save(buffer, format=output_format, quality=jpeg_quality, optimize=True)
        else:
            image.save(buffer, format=output_format)
        
        return buffer.getvalue(), filename
    
    def get_export_info(self, image: Image.Image, settings: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about the exported image.
        
        Args:
            image: PIL Image
            settings: Export settings
            
        Returns:
            Dictionary with export information
        """
        output_format = settings.get('output_format', 'PNG')
        
        return {
            'dimensions': f"{image.width} x {image.height}",
            'format': output_format,
            'mode': image.mode,
            'size_estimate': f"~{(image.width * image.height * 3) // 1024}KB"
        }
    
    def _align_images(self, images: List[np.ndarray]) -> List[np.ndarray]:
        """
        Align images using feature matching (simplified implementation).
        
        Args:
            images: List of numpy arrays
            
        Returns:
            List of aligned numpy arrays
        """
        # For now, return as-is (basic implementation)
        # In a full implementation, you'd use ORB/SIFT feature matching
        return images
    
    def _upscale_image(self, image: Image.Image, factor: float) -> Image.Image:
        """
        Upscale image using high-quality resampling.
        
        Args:
            image: PIL Image to upscale
            factor: Upscale factor
            
        Returns:
            Upscaled PIL Image
        """
        new_width = int(image.width * factor)
        new_height = int(image.height * factor)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """
        Apply image enhancement (sharpening, contrast, etc.).
        
        Args:
            image: PIL Image to enhance
            
        Returns:
            Enhanced PIL Image
        """
        # Apply subtle sharpening
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        # Apply subtle contrast enhancement
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.05)
        
        return image