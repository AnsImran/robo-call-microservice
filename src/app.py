import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.api.v1.router import api_router
from src.core.config import settings
from src.core.exceptions import RoboCallError
from src.core.logging import request_id_ctx, setup_logging
from src.middleware.request_context import RequestContextMiddleware
from src.schemas.errors import ErrorResponse

logger = logging.getLogger(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    setup_logging(settings.LOG_LEVEL)
    logger.info(
        "Starting %s v%s env=%s",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.APP_ENV,
    )
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production microservice for placing outbound Twilio TTS calls.",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(RequestContextMiddleware)

    @app.exception_handler(RoboCallError)
    async def robo_error_handler(request: Request, exc: RoboCallError) -> JSONResponse:
        logger.warning("%s: %s", exc.__class__.__name__, exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=exc.__class__.__name__,
                detail=exc.detail,
                request_id=request_id_ctx.get(),
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error="ValidationError",
                detail=str(exc.errors()),
                request_id=request_id_ctx.get(),
            ).model_dump(),
        )

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
