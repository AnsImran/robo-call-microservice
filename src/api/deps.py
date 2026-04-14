from functools import lru_cache

from src.core.config import get_settings
from src.services.twilio_service import TwilioCallService


@lru_cache
def get_twilio_service() -> TwilioCallService:
    return TwilioCallService(get_settings())
