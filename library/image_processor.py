from rembg import remove
from PIL import Image
import io
from typing import Tuple


class ImageProcessor:
    def remove_background(self, image_data: bytes) -> bytes:
        """Simple background removal"""
        return remove(image_data)

    def process_and_convert(
        self, image_data: bytes, output_format: str = "PNG"
    ) -> Tuple[bytes, str]:
        """
        Process image and convert to desired format

        Args:
            image_data: Input image as bytes
            output_format: Output format (PNG, JPEG, etc.)

        Returns:
            Tuple of (processed image bytes, mime type)
        """
        # Process image
        processed_data = self.remove_background(image_data)

        # Convert to desired format
        img = Image.open(io.BytesIO(processed_data))

        # Handle format conversion
        output_format = output_format.upper()
        mime_type = f"image/{output_format.lower()}"

        # Save to bytes
        output_bytes = io.BytesIO()
        img.save(output_bytes, format=output_format)
        output_bytes.seek(0)

        return output_bytes.getvalue(), mime_type

    def replace_background(
        self, image_data: bytes, background_color: tuple = (255, 255, 255)
    ) -> Tuple[bytes, str]:
        """Remove background and replace with a solid color instead of transparency"""
        # Process image to remove background
        processed_data = self.remove_background(image_data)
        img = Image.open(io.BytesIO(processed_data))

        # Create a new image with the specified background color
        if img.mode == "RGBA":
            background = Image.new("RGBA", img.size, background_color + (255,))
            composite = Image.alpha_composite(background, img)
        else:
            background = Image.new("RGB", img.size, background_color)
            composite = img

        # Save to bytes
        output_bytes = io.BytesIO()
        composite.save(output_bytes, format="PNG")
        output_bytes.seek(0)

        return output_bytes.getvalue(), "image/png"
