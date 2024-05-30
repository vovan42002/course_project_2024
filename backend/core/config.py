from envparse import Env

env = Env()

PROJECT_NAME = "Cinema Booking System"
PROJECT_DESCRIPTION = "Fast API application for cinemas which support full cycle of ticket reservation and can be used as backend for production systems"
VERSION = "0.0.1"

SECRET_KEY: str = env.str(
    "SECRET_KEY",
    default="18f4e284c20f7efd72e85380a2ef7c71dca25a7a797ce7de093201a3bd3e83e8",
)
API_VERSION: str = env.str("API_VERSION", default="/v1")

SQLALCHEMY_DATABASE_URI: str = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:password@postgres:5432/booking-db",
)
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=60)


ADMIN_USERNAME: str = env.str("ADMIN_USERNAME", default="admin")
ADMIN_PASSWORD: str = env.str("ADMIN_PASSWORD", default="password")
ADMIN_EMAIL: str = env.str("ADMIN_EMAIL", default="admin@gmail.com")
ADMIN_FIRST_NAME: str = env.str("ADMIN_FIRST_NAME", default="John")
ADMIN_LAST_NAME: str = env.str("ADMIN_LAST_NAME", default="Doe")

CELERY_BROKER_URL: str = env.str("CELERY_BROKER_URL", default="")
CELERY_RESULT_BACKEND_URL: str = env.str("CELERY_RESULT_BACKEND_URL", default="")

EMAIL_SENDER: str = env.str("EMAIL_SENDER", default="")
EMAIL_SENDER_PASSWORD: str = env.str("EMAIL_SENDER_PASSWORD", default="")
