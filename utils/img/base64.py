"""
Base64 image utils.
"""
import base64
from io import BytesIO

from PIL import Image
from PIL.Image import Image


class Base64Image:
    @classmethod
    def encode(cls, img: Image, format: str = 'PNG') -> str:
        buffered = BytesIO()
        img.save(buffered, format)
        img_bytes = buffered.getvalue()
        img_str = base64.b64encode(img_bytes)
        return str(img_str)

    @classmethod
    def decode_file(cls, base64_img: str) -> BytesIO:
        img_bytes = base64.b64decode(base64_img)
        return BytesIO(img_bytes)

    @classmethod
    def decode(cls, base64_img: str, format: str = 'PNG') -> Image:
        image_file = Base64Image.decode_file(base64_img)
        return Image.open(image_file, formats=[format])
