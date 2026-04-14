from fastapi import APIRouter, Depends, status

from src.api.deps import get_twilio_service
from src.schemas.call import CallRequest, CallResponse
from src.schemas.errors import ErrorResponse
from src.services.twilio_service import TwilioCallService

router = APIRouter(prefix="/calls", tags=["calls"])


@router.post(
    "",
    response_model=CallResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Place a TTS robo-call",
    description=(
        "Places an outbound voice call via Twilio and plays the supplied "
        "`message` to the recipient using text-to-speech."
    ),
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        502: {"model": ErrorResponse, "description": "Upstream Twilio error"},
    },
)
def place_call(
    payload: CallRequest,
    svc: TwilioCallService = Depends(get_twilio_service),
) -> CallResponse:
    result = svc.place_tts_call(to=payload.to, message=payload.message)
    return CallResponse.model_validate(result)
