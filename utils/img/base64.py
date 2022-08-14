"""
Base64 image utils.
"""
import base64
from io import BytesIO

from PIL import Image
from PIL.Image import Image as ImageEntity


class Base64Image:
    @classmethod
    def encode(cls, img: ImageEntity, format: str = 'PNG') -> str:
        buffered = BytesIO()
        img.save(buffered, format)
        img_bytes = buffered.getvalue()
        base64_img = base64.b64encode(img_bytes)
        return base64_img.decode()

    @classmethod
    def decode_file(cls, base64_img: str) -> BytesIO:
        img_bytes = base64.b64decode(base64_img)
        return BytesIO(img_bytes)

    @classmethod
    def decode(cls, base64_img: str, format: str = 'PNG') -> ImageEntity:
        img_file = Base64Image.decode_file(base64_img)
        return Image.open(img_file, formats=[format])
