# Robo Call Service

A production-grade FastAPI microservice that places outbound voice calls via Twilio and plays a supplied message using text-to-speech.

## Features
- FastAPI application factory with lifespan
- Pydantic v2 schemas with full validation (E.164 phone, message length)
- Versioned API (`/api/v1`)
- Service layer + dependency injection (Twilio client is mockable)
- Structured logging with per-request `X-Request-ID`
- CORS, rate limiting (slowapi), global exception handlers
- Health endpoint for liveness probes
- Dockerized, tested (pytest + mocked Twilio)

## Setup

```bash
cp .env.example .env
# edit .env with your Twilio credentials
pip install -e ".[dev]"
```

## Run

```bash
python main.py
# or
make run
```

Then open http://localhost:8000/docs for the Swagger UI.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/health` | Liveness probe |
| POST | `/api/v1/calls` | Place a TTS call |

### Example

```bash
curl -X POST http://localhost:8000/api/v1/calls \
  -H "Content-Type: application/json" \
  -d '{"to":"+19494248180","message":"Hello from the robo call service"}'
```

Response:
```json
{
  "call_sid": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "status": "queued",
  "to": "+19494248180",
  "from_number": "+18339213517"
}
```

## Environment Variables

| Var | Required | Default | Description |
|---|---|---|---|
| `TWILIO_ACCOUNT_SID` | yes | — | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | yes | — | Twilio Auth Token |
| `TWILIO_FROM_NUMBER` | yes | — | Your Twilio phone number (E.164) |
| `APP_ENV` | no | `development` | `development` / `staging` / `production` |
| `LOG_LEVEL` | no | `INFO` | Python log level |
| `HOST` | no | `0.0.0.0` | Bind host |
| `PORT` | no | `8000` | Bind port |
| `CORS_ORIGINS` | no | `["*"]` | Allowed CORS origins (JSON list) |
| `RATE_LIMIT_PER_MINUTE` | no | `30` | Per-IP rate limit |

## Tests

```bash
make test
```

Tests use `dependency_overrides` to mock the Twilio service — no real calls are placed.

## Docker

```bash
make docker
docker run --rm -p 8000:8000 --env-file .env robo-call-service
```

## Notes
- Trial Twilio accounts can only call **verified** recipient numbers.
- Using `client.calls.create(twiml=...)` (not Studio Flow) — supports dynamic per-request TTS text and avoids Studio's per-execution surcharge.
