import logging

from fastapi import Depends


from celery_app import celery_app
from celery.exceptions import SoftTimeLimitExceeded
from celery.states import SUCCESS, STARTED
from celery.result import AsyncResult
from core import config
from core.hashing import Hasher
from db.dals import UserDAL
from db.session import get_db2
from sqlalchemy.ext.asyncio import AsyncSession
from celery.signals import worker_ready
import asyncio
from api import models


logger = logging.getLogger(__name__)


@worker_ready.connect
def at_start(sender, **kwargs):
    async def init_admin_user():
        logger.info("Start celery task to init admin user")
        try:
            async with get_db2() as session:
                user_dal = UserDAL(session)
                user_created = await user_dal.get_user_by_email(
                    email=config.ADMIN_EMAIL
                )
                if not user_created:
                    user = await user_dal.create_user(
                        email=config.ADMIN_EMAIL,
                        first_name=config.ADMIN_FIRST_NAME,
                        last_name=config.ADMIN_LAST_NAME,
                        hashed_password=Hasher.get_password_hash(config.ADMIN_PASSWORD),
                        is_superuser=True,
                    )
                    logger.info(f"Created user: {user.email}")

                    await session.commit()  # Ensure the transaction is committed

                    if user is not None:
                        return True
                else:
                    logger.info("Admin user %s already exists", config.ADMIN_EMAIL)
        except Exception as e:
            logger.error(f"Failed to create admin user: {e}")
            await session.rollback()  # Explicitly roll back in case of error

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_admin_user())
