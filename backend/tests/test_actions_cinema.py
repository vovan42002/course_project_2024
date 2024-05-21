import pytest
from unittest.mock import patch
from actions.cinema import _create, _delete, _update, _get_by_id, _get_all
from api.models import AllCinemasShow


@pytest.mark.asyncio
async def test_create_success(session, cinema_create, cinema_show):
    with patch("db.dals.CinemaDAL.create", return_value=cinema_show):
        result = await _create(cinema_create, session)
    assert result == cinema_show


@pytest.mark.asyncio
async def test_create_none(session, cinema_create):
    result = await _create(cinema_create, session)
    assert result is None


@pytest.mark.asyncio
async def test_delete_success(session):
    with patch("db.dals.CinemaDAL.delete", return_value=1):
        result = await _delete(1, session)
    assert result == 1


@pytest.mark.asyncio
async def test_delete_none(session):
    with patch("db.dals.CinemaDAL.delete", return_value=None):
        result = await _delete(1, session)
    assert result is None


@pytest.mark.asyncio
async def test_update_success(session, cinema_update_req):
    with patch("db.dals.CinemaDAL.update", return_value=1):
        result = await _update(cinema_update_req, 1, session)
    assert result == 1


@pytest.mark.asyncio
async def test_update_none(session, cinema_update_req):
    with patch("db.dals.CinemaDAL.update", return_value=None):
        result = await _update(cinema_update_req, 1, session)
    assert result == None


@pytest.mark.asyncio
async def test_get_by_id_success(session, cinema_show):
    with patch("db.dals.CinemaDAL.get_by_id", return_value=cinema_show):
        result = await _get_by_id(1, session)
    assert result == cinema_show


@pytest.mark.asyncio
async def test_get_by_id_none(session):
    with patch("db.dals.CinemaDAL.get_by_id", return_value=None):
        result = await _get_by_id(1, session)
    assert result == None


@pytest.mark.asyncio
async def test_get_all_success(session, cinema_show, all_cinemas_show):
    with patch("db.dals.CinemaDAL.get_all_active", return_value=[cinema_show]):
        result = await _get_all(session)
    assert len(result.result) == 1
    assert result == all_cinemas_show


@pytest.mark.asyncio
async def test_get_all_none(session):
    with patch("db.dals.CinemaDAL.get_all_active", return_value=[]):
        result = await _get_all(session)
    assert len(result.result) == 0
    assert result == AllCinemasShow(result=[])
