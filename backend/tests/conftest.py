from fastapi.testclient import TestClient
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from actions.auth import get_current_user_from_token
from api.models import CinemaCreate, CinemaShow, AllCinemasShow, CinemaUpdateRequest
from db.models import Cinema, User
from fastapi import FastAPI
from db.session import get_db
from main import app
import copy


# Setup mock data
cinema_data = {
    "name": "Cinema One",
    "description": "A description",
    "is_active": True,
    "created_at": datetime(2024, 1, 1, 5, 0, 0),
    "updated_at": datetime(2024, 1, 1, 5, 0, 0),
}

user = User(
    id=1,
    email="test@test.com",
    hashed_password="$2b$12$/a8arxE20/wSAoUkK6QOauVstLzJS8yMgAPgbZunnY.g2gAaAxEA6",
    is_active=True,
    is_vendor=False,
    is_superuser=True,
)


@pytest.fixture
def user_mock():
    return user


@pytest.fixture
def override_dependencies():
    app.dependency_overrides[get_current_user_from_token] = lambda: user
    app.dependency_overrides[get_db] = lambda: AsyncMock()
    yield

    del app.dependency_overrides[get_current_user_from_token]
    del app.dependency_overrides[get_db]


@pytest.fixture
def override_dependencie_get_db():
    app.dependency_overrides[get_db] = lambda: AsyncMock()
    yield

    del app.dependency_overrides[get_db]


@pytest.fixture
def override_dependencie_get_current_user_from_token():
    copy_user = copy.deepcopy(user)
    copy_user.is_superuser = False
    app.dependency_overrides[get_current_user_from_token] = lambda: copy_user
    yield

    del app.dependency_overrides[get_current_user_from_token]


@pytest.fixture
def cinema_create():
    return CinemaCreate(name="Cinema One", description="A description").copy()


@pytest.fixture
def cinema_show():
    return CinemaShow(**cinema_data).copy()


@pytest.fixture
def all_cinemas_show():
    return AllCinemasShow(result=[CinemaShow(**cinema_data)])


@pytest.fixture
def session():
    return MagicMock()


@pytest.fixture
def cinema_update_req():
    return CinemaUpdateRequest(name="Updated cinema").copy()


@pytest.fixture
def async_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def cinema():
    return Cinema(
        id=1,
        name="Cinema One",
        description="A description",
        is_active=True,
        created_at=datetime(2024, 1, 1, 5, 0, 0),
        updated_at=datetime(2024, 1, 1, 5, 0, 0),
    )


@pytest.fixture()
def test_app():
    return app


@pytest.fixture
def client(test_app: FastAPI):
    return TestClient(test_app)
