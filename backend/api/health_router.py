from fastapi import APIRouter, status
from api.models import HealthCheckResponse

health_router = APIRouter()


@health_router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
)
async def health_status():
    """
    This method allows to check the service health
    """
    return {"status": "OK"}
