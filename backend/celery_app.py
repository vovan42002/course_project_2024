from celery import Celery
from core import config

celery_app = Celery(
    __name__,
    include=["tasks"],
    backend=config.CELERY_RESULT_BACKEND_URL,
    broker=config.CELERY_BROKER_URL,
)
