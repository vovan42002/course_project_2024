from datetime import datetime
from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient
from fastapi import status
from api.models import AllCinemasShow, CinemaShow, CinemaUpdateRequest
from main import app


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_dependencie_get_db")
async def test_create_cinema_unathorized():
    cinema_data = {"name": "Cinema One", "description": "A description"}

    # Ensure _create returns a coroutine with the correct result
    with patch("api.cinema_router._create", new_callable=AsyncMock) as mock_create:
        with patch("core.permissions.check_role", return_value=True):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.post("/v1/cinema/", json=cinema_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "override_dependencie_get_db",
    "override_dependencie_get_current_user_from_token",
)
async def test_create_cinema_unathorized():
    cinema_data = {"name": "Cinema One", "description": "A description"}

    # Ensure _create returns a coroutine with the correct result
    with patch("api.cinema_router._create", new_callable=AsyncMock) as mock_create:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/v1/cinema/", json=cinema_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_dependencies")
async def test_create_cinema(cinema_show):
    cinema_data = {"name": "Cinema One", "description": "A description"}

    # Ensure _create returns a coroutine with the correct result
    with patch("api.cinema_router._create", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = cinema_show
        with patch("core.permissions.check_role", return_value=True):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.post("/v1/cinema/", json=cinema_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Cinema One"
    assert response.json()["description"] == "A description"


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_dependencies")
async def test_delete_cinema():
    cinema_id = 1
    with patch("api.cinema_router._delete", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = cinema_id
        with patch("core.permissions.check_role", return_value=True):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.delete(f"/v1/cinema/{cinema_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"cinema_id": cinema_id}


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_dependencies")
async def test_get_cinema_by_id():
    cinema_id = 1
    cinema_show = CinemaShow(
        name="Cinema One",
        description="A description",
        is_active=True,
        updated_at=datetime(2024, 1, 1, 5, 0),
        created_at=datetime(2024, 1, 1, 5, 0),
    )

    # Ensure _get_by_id returns a coroutine with the correct result
    with patch(
        "api.cinema_router._get_by_id", new_callable=AsyncMock
    ) as mock_get_by_id:
        mock_get_by_id.return_value = cinema_show
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/v1/cinema/{cinema_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": cinema_show.name,
        "description": cinema_show.description,
        "is_active": cinema_show.is_active,
        "updated_at": cinema_show.updated_at.isoformat(),
        "created_at": cinema_show.created_at.isoformat(),
    }


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_dependencies")
async def test_get_all_cinemas(client):
    cinemas_show = AllCinemasShow(
        result=[
            CinemaShow(
                name="Cinema One",
                description="A description",
                is_active=True,
                updated_at=datetime(2024, 1, 1, 5, 0),
                created_at=datetime(2024, 1, 1, 5, 0),
            ),
            CinemaShow(
                name="Cinema Two",
                description="Another description",
                is_active=True,
                updated_at=datetime(2024, 1, 2, 5, 0),
                created_at=datetime(2024, 1, 2, 5, 0),
            ),
        ]
    )

    # Ensure _get_all returns a coroutine with the correct result
    with patch("api.cinema_router._get_all", new_callable=AsyncMock) as mock_get_all:
        mock_get_all.return_value = cinemas_show
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/v1/cinema/all")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "result": [
            {
                "name": "Cinema One",
                "description": "A description",
                "is_active": True,
                "updated_at": "2024-01-01T05:00:00",
                "created_at": "2024-01-01T05:00:00",
            },
            {
                "name": "Cinema Two",
                "description": "Another description",
                "is_active": True,
                "updated_at": "2024-01-02T05:00:00",
                "created_at": "2024-01-02T05:00:00",
            },
        ]
    }


@pytest.mark.asyncio
@pytest.mark.usefixtures("override_dependencies")
async def test_update_cinema_by_id(client):
    cinema_id = 1
    update_data = CinemaUpdateRequest(name="Updated Cinema")

    with patch(
        "api.cinema_router._get_by_id", new_callable=AsyncMock
    ) as mock_get_by_id:
        mock_get_by_id.return_value = {
            "id": cinema_id,
            "name": "Old Cinema",
            "description": "Old description",
            "is_active": True,
            "updated_at": datetime(2024, 1, 1, 5, 0),
            "created_at": datetime(2024, 1, 1, 5, 0),
        }

        # Ensure _update returns the ID of the updated cinema
        with patch("api.cinema_router._update", new_callable=AsyncMock) as mock_update:
            mock_update.return_value = cinema_id

            # Ensure check_role returns True to bypass permissions
            with patch("core.permissions.check_role", return_value=True):
                async with AsyncClient(app=app, base_url="http://test") as ac:
                    response = await ac.patch(
                        f"/v1/cinema/{cinema_id}", json=update_data.dict()
                    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"cinema_id": cinema_id}
