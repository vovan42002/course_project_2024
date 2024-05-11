from typing import Union

from api.models import CinemaCreate, CinemaShow
from db.dals import CinemaDAL


async def _create(body: CinemaCreate, session) -> Union[CinemaShow, None]:
    async with session.begin():
        cinema_dal = CinemaDAL(session)
        cinema = await cinema_dal.create(
            name=body.name,
            description=body.description,
        )
        if cinema is not None:
            return CinemaShow(
                name=cinema.name,
                description=cinema.description,
                is_active=cinema.is_active,
                created_at=cinema.created_at,
                updated_at=cinema.updated_at,
            )


async def _delete(cinema_id, session) -> Union[int, None]:
    async with session.begin():
        cinema_dal = CinemaDAL(session)
        deleted_cinema = await cinema_dal.delete(cinema_id=cinema_id)
        return deleted_cinema


async def _update(
    updated_cinema_params: dict, cinema_id: int, session
) -> Union[int, None]:
    async with session.begin():
        cinema_dal = CinemaDAL(session)
        updated_cinema = await cinema_dal.update(
            cinema_id, **updated_cinema_params.dict()
        )
        return updated_cinema


async def _get_by_id(cinema_id, session) -> Union[CinemaShow, None]:
    async with session.begin():
        cinema_dal = CinemaDAL(session)
        cinema = await cinema_dal.get_by_id(cinema_id=cinema_id)
        if cinema is not None:
            return CinemaShow(
                name=cinema.name,
                description=cinema.description,
                is_active=cinema.is_active,
                created_at=cinema.created_at,
                updated_at=cinema.updated_at,
            )
