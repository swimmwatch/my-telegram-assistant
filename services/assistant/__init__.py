"""
Assistant service package.
"""
from services.assistant.config import AIOTDLIB_API_ID, AIOTDLIB_API_HASH, PHONE_NUMBER
from utils.aiotdlib.client import CustomClient

aiotdlib_client = CustomClient(
    api_id=AIOTDLIB_API_ID,
    api_hash=AIOTDLIB_API_HASH,
    phone_number=PHONE_NUMBER,
)
