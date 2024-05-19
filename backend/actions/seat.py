from typing import Union

from api.models import AllSeatsShow, SeatCreate, SeatShow
from db.dals import SeatDAL


async def _create(body: SeatCreate, session) -> Union[SeatShow, None]:
    async with session.begin():
        seat_dal = SeatDAL(session)
        seat = await seat_dal.create(
            number=body.number,
            hall_id=body.hall_id,
        )
        if seat is not None:
            return SeatShow(
                number=body.number,
                hall_id=body.hall_id,
                is_active=seat.is_active,
                created_at=seat.created_at,
                updated_at=seat.updated_at,
            )


async def _delete(seat_id, session) -> Union[int, None]:
    async with session.begin():
        seat_dal = SeatDAL(session)
        deleted_seat = await seat_dal.delete(seat_id=seat_id)
        return deleted_seat


async def _update(updated_seat_params: dict, seat_id: int, session) -> Union[int, None]:
    async with session.begin():
        seat_dal = SeatDAL(session)
        updated_seat = await seat_dal.update(seat_id, **updated_seat_params.dict())
        return updated_seat


async def _get_by_id(seat_id, session) -> Union[SeatShow, None]:
    async with session.begin():
        seat_dal = SeatDAL(session)
        seat = await seat_dal.get_by_id(seat_id=seat_id)
        if seat is not None:
            return SeatShow(
                number=seat.number,
                hall_id=seat.hall_id,
                is_active=seat.is_active,
                created_at=seat.created_at,
                updated_at=seat.updated_at,
            )


async def _get_all(session) -> Union[AllSeatsShow, None]:
    async with session.begin():
        seat_dal = SeatDAL(session)
        seats = await seat_dal.get_all_active()
        seats_show = []
        if seats is not None:
            for seat in seats:
                seats_show.append(
                    SeatShow(
                        number=seat.number,
                        hall_id=seat.hall_id,
                        is_active=seat.is_active,
                        created_at=seat.created_at,
                        updated_at=seat.updated_at,
                    )
                )
            return AllSeatsShow(result=seats_show)
