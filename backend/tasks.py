import logging

from celery_app import celery_app
from celery.exceptions import SoftTimeLimitExceeded
from celery.states import SUCCESS, STARTED
from celery.result import AsyncResult
from core import config


logger = logging.getLogger(__name__)


@celery_app.task(
    name="Create book",
    queue="booking",
)
def add_book(self, request_data: str):
    logger.info("Start main background celery task book")
    return True
