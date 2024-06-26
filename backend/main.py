from fastapi import FastAPI
from core import config

from api.login_router import login_router
from api.user_router import user_router
from api.health_router import health_router
from api.cinema_router import cinema_router
from api.hall_router import hall_router
from api.movie_router import movie_router
from api.showing_router import showing_router
from api.seat_router import seat_router
from api.book_router import book_router


app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    debug=True,
    description=config.PROJECT_DESCRIPTION,
)


app.include_router(prefix="/test", router=health_router)
app.include_router(prefix=config.API_VERSION, router=login_router)
app.include_router(prefix=config.API_VERSION, router=user_router)
app.include_router(prefix=config.API_VERSION, router=cinema_router)
app.include_router(prefix=config.API_VERSION, router=hall_router)
app.include_router(prefix=config.API_VERSION, router=movie_router)
app.include_router(prefix=config.API_VERSION, router=showing_router)
app.include_router(prefix=config.API_VERSION, router=seat_router)
app.include_router(prefix=config.API_VERSION, router=book_router)
