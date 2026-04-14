class RoboCallError(Exception):
    """Base application error with HTTP status and user-safe detail."""

    status_code: int = 500
    default_detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.default_detail
        super().__init__(self.detail)


class TwilioProviderError(RoboCallError):
    status_code = 502
    default_detail = "Upstream Twilio error"


class InvalidRequestError(RoboCallError):
    status_code = 400
    default_detail = "Invalid request"
