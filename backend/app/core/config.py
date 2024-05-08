import os

PROJECT_NAME = "Cinema Booking System"
PROJECT_DESCRIPTION = "Fast API application for cinemas which support full cycle of ticket reservation and can be used as backend for production systems"
VERSION = "0.0.1"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
