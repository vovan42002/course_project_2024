from fastapi import FastAPI, APIRouter, status
import core.schemas as schemas
import uvicorn
import core.config as config


app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    debug=True,
    description=config.PROJECT_DESCRIPTION,
)

router_test = APIRouter(prefix="/test")


@router_test.get(
    "/health",
    response_model=schemas.HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
)
async def health_status():
    """
    This method allows to check the service health
    """
    return {"status": "OK"}


app.include_router(router=router_test)

uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=8000,
)
