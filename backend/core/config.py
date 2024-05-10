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

SQLALCHEMY_DATABASE_URI: str = env.str("DATABASE_URL")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=60)
