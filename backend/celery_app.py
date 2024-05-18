from celery import Celery
from core import config

celery_app = Celery(__name__, include=["tasks"])
celery_app.conf.broker_url = config.CELERY_BROKER_URL
celery_app.conf.result_backend = config.CELERY_RESULT_BACKEND_URL
