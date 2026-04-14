import logging

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

from src.core.config import Settings
from src.core.exceptions import TwilioProviderError

logger = logging.getLogger(__name__)


class TwilioCallService:
    """Thin wrapper around the Twilio REST client for placing TTS calls."""

    def __init__(self, settings: Settings) -> None:
        self._from_number = settings.TWILIO_FROM_NUMBER
        self._client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

    def place_tts_call(self, to: str, message: str) -> dict[str, str]:
        twiml = VoiceResponse()
        twiml.say(message)
        try:
            call = self._client.calls.create(
                to=to,
                from_=self._from_number,
                twiml=str(twiml),
            )
        except TwilioRestException as e:
            logger.exception("Twilio rejected call to %s", to)
            raise TwilioProviderError(detail=str(e)) from e

        logger.info("Placed call sid=%s to=%s status=%s", call.sid, to, call.status)
        return {
            "call_sid": call.sid,
            "status": call.status or "queued",
            "to": to,
            "from_number": self._from_number,
        }
