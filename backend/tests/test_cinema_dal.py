import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from db.dals import CinemaDAL
from db.models import Cinema


@pytest.mark.asyncio
async def test_create(async_session, cinema):
    cinema_dal = CinemaDAL(async_session)
    async_session.flush = AsyncMock()

    result = await cinema_dal.create(name=cinema.name, description=cinema.description)

    async_session.add.assert_called_once()
    async_session.flush.assert_called_once()
    assert result.name == cinema.name
    assert result.description == cinema.description
    assert isinstance(result, Cinema)


@pytest.mark.asyncio
async def test_delete(async_session):
    async_session.execute = AsyncMock(
        return_value=AsyncMock(fetchone=MagicMock(return_value=[1]))
    )
    cinema_dal = CinemaDAL(async_session)
    result = await cinema_dal.delete(cinema_id=1)
    assert result == 1


@pytest.mark.asyncio
async def test_update(async_session):
    async_session.execute = AsyncMock(
        return_value=AsyncMock(fetchone=MagicMock(return_value=[1]))
    )
    cinema_dal = CinemaDAL(async_session)
    result = await cinema_dal.update(cinema_id=1, name="Updated Cinema")
    assert result == 1
    async_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id(async_session, cinema):
    async_session.execute = AsyncMock(
        return_value=AsyncMock(fetchone=MagicMock(return_value=[cinema]))
    )
    cinema_dal = CinemaDAL(async_session)

    result = await cinema_dal.get_by_id(cinema_id=cinema.id)

    assert result == cinema
    async_session.execute.assert_called_once()
