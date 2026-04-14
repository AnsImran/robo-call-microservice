from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

PhoneNumber = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=r"^\+[1-9]\d{1,14}$",
    ),
]


class CallRequest(BaseModel):
    """Payload for placing an outbound TTS voice call."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "examples": [
                {
                    "to": "+19494248180",
                    "message": "Hello! This is a reminder about your appointment tomorrow.",
                }
            ]
        },
    )

    to: PhoneNumber = Field(
        ...,
        description=(
            "Recipient phone number in E.164 format (leading '+' and country code). "
            "On Twilio trial accounts this must be a pre-verified number."
        ),
        examples=["+19494248180"],
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description=(
            "Text to be spoken to the recipient via Twilio TTS. "
            "Capped at 1000 characters to avoid abuse and TTS truncation."
        ),
        examples=["Hello! This is a reminder about your appointment tomorrow."],
    )


class CallResponse(BaseModel):
    """Result of a successfully queued outbound call."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "call_sid": "CAf9f1e93fdd78dad37f1ff1c40026d94a",
                    "status": "queued",
                    "to": "+19494248180",
                    "from_number": "+18339213517",
                }
            ]
        }
    )

    call_sid: str = Field(
        ...,
        description="Unique Twilio Call SID identifying the placed call.",
        examples=["CAf9f1e93fdd78dad37f1ff1c40026d94a"],
    )
    status: str = Field(
        ...,
        description="Initial call status returned by Twilio (typically 'queued').",
        examples=["queued"],
    )
    to: PhoneNumber = Field(
        ...,
        description="Recipient phone number (E.164).",
        examples=["+19494248180"],
    )
    from_number: PhoneNumber = Field(
        ...,
        description="Twilio caller-ID used to place the call (E.164).",
        examples=["+18339213517"],
    )
