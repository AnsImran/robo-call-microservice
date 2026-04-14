from fastapi import APIRouter

from src.core.config import settings
from src.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns service metadata. Used by k8s/load balancers as a liveness probe.",
)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    )
