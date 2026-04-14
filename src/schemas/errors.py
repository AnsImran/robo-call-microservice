from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    """Uniform error envelope returned by all failing endpoints."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "error": "TwilioProviderError",
                    "detail": "Twilio rejected the call: invalid 'To' number.",
                    "request_id": "3f8b0a9c1e7a4d2b9f0e6c5d4a3b2c1d",
                }
            ]
        }
    )

    error: str = Field(
        ...,
        description="Machine-readable error class name.",
        examples=["TwilioProviderError"],
    )
    detail: str = Field(
        ...,
        description="Human-readable error description.",
        examples=["Twilio rejected the call: invalid 'To' number."],
    )
    request_id: str | None = Field(
        default=None,
        description="Request ID (matches X-Request-ID header) for tracing in logs.",
        examples=["3f8b0a9c1e7a4d2b9f0e6c5d4a3b2c1d"],
    )
