from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from src.api.deps import get_twilio_service
from src.app import app


@pytest.fixture
def twilio_mock() -> MagicMock:
    mock = MagicMock()
    mock.place_tts_call.return_value = {
        "call_sid": "CAtest0000000000000000000000000001",
        "status": "queued",
        "to": "+19494248180",
        "from_number": "+18339213517",
    }
    return mock


@pytest.fixture
def client(twilio_mock: MagicMock) -> Iterator[TestClient]:
    app.dependency_overrides[get_twilio_service] = lambda: twilio_mock
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
