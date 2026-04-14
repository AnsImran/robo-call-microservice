from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """Liveness probe response."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "ok",
                    "service": "Robo Call Service",
                    "version": "0.1.0",
                    "environment": "development",
                }
            ]
        }
    )

    status: Literal["ok"] = Field(..., description="Service health status.", examples=["ok"])
    service: str = Field(..., description="Service name.", examples=["Robo Call Service"])
    version: str = Field(..., description="Service version (semver).", examples=["0.1.0"])
    environment: str = Field(
        ..., description="Deployment environment.", examples=["development"]
    )
