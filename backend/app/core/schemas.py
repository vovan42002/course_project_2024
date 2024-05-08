from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """
    A response model for the health check
    """

    status: str = Field(
        ...,
        title="Status",
        description="A status of the service",
        example="OK",
    )
