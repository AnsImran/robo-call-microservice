from unittest.mock import MagicMock

from fastapi.testclient import TestClient


def test_place_call_success(client: TestClient, twilio_mock: MagicMock) -> None:
    r = client.post(
        "/api/v1/calls",
        json={"to": "+19494248180", "message": "Hello from the robo call service"},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["call_sid"] == "CAtest0000000000000000000000000001"
    assert body["status"] == "queued"
    assert body["to"] == "+19494248180"
    assert body["from_number"] == "+18339213517"
    twilio_mock.place_tts_call.assert_called_once_with(
        to="+19494248180", message="Hello from the robo call service"
    )


def test_place_call_invalid_phone_missing_plus(client: TestClient) -> None:
    r = client.post(
        "/api/v1/calls",
        json={"to": "19494248180", "message": "hi"},
    )
    assert r.status_code == 422
    body = r.json()
    assert body["error"] == "ValidationError"
    assert "request_id" in body


def test_place_call_empty_message(client: TestClient) -> None:
    r = client.post(
        "/api/v1/calls",
        json={"to": "+19494248180", "message": ""},
    )
    assert r.status_code == 422


def test_place_call_message_too_long(client: TestClient) -> None:
    r = client.post(
        "/api/v1/calls",
        json={"to": "+19494248180", "message": "x" * 1001},
    )
    assert r.status_code == 422
