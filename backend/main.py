from fastapi import FastAPI, APIRouter, status
from core import config

from api.login_router import login_router
from api.user_router import user_router
from api.health_router import health_router


app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    debug=True,
    description=config.PROJECT_DESCRIPTION,
)


app.include_router(prefix="/test", router=health_router)
app.include_router(prefix=config.API_VERSION, router=login_router)
app.include_router(prefix=config.API_VERSION, router=user_router)
