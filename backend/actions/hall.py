from typing import Union

from api.models import HallCreate, HallShow
from db.dals import HallDAL


async def _create(body: HallCreate, session) -> Union[HallShow, None]:
    async with session.begin():
        hall_dal = HallDAL(session)
        hall = await hall_dal.create(
            name=body.name,
            description=body.description,
            cinema_id=body.cinema_id,
        )
        if hall is not None:
            return HallShow(
                name=hall.name,
                description=hall.description,
                is_active=hall.is_active,
                created_at=hall.created_at,
                updated_at=hall.updated_at,
            )


async def _delete(hall_id, session) -> Union[int, None]:
    async with session.begin():
        hall_dal = HallDAL(session)
        deleted_hall = await hall_dal.delete(hall_id=hall_id)
        return deleted_hall


async def _update(updated_hall_params: dict, hall_id: int, session) -> Union[int, None]:
    async with session.begin():
        hall_dal = HallDAL(session)
        updated_hall = await hall_dal.update(hall_id, **updated_hall_params.dict())
        return updated_hall


async def _get_by_id(hall_id, session) -> Union[HallShow, None]:
    async with session.begin():
        hall_dal = HallDAL(session)
        hall = await hall_dal.get_by_id(hall_id=hall_id)
        if hall is not None:
            return HallShow(
                name=hall.name,
                description=hall.description,
                is_active=hall.is_active,
                created_at=hall.created_at,
                updated_at=hall.updated_at,
            )
