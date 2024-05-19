from typing import Union

from api.models import AllShowingsShow, ShowingCreate, ShowingShow
from db.dals import ShowingDAL


async def _create(body: ShowingCreate, session) -> Union[ShowingShow, None]:
    async with session.begin():
        showing_dall = ShowingDAL(session)
        showing = await showing_dall.create(
            title=body.title,
            start=body.start,
            end=body.end,
            hall_id=body.hall_id,
            movie_id=body.movie_id,
        )
        if showing is not None:
            return ShowingShow(
                title=showing.title,
                start=showing.start,
                end=showing.end,
                hall_id=showing.hall_id,
                movie_id=showing.movie_id,
                is_active=showing.is_active,
                created_at=showing.created_at,
                updated_at=showing.updated_at,
            )


async def _delete(showing_id, session) -> Union[int, None]:
    async with session.begin():
        showing_dall = ShowingDAL(session)
        deleted_showing = await showing_dall.delete(showing_id=showing_id)
        return deleted_showing


async def _update(
    updated_showing_params: dict, showing_id: int, session
) -> Union[int, None]:
    async with session.begin():
        showing_dall = ShowingDAL(session)
        updated_showing = await showing_dall.update(
            showing_id, **updated_showing_params.dict()
        )
        return updated_showing


async def _get_by_id(showing_id, session) -> Union[ShowingShow, None]:
    async with session.begin():
        showing_dall = ShowingDAL(session)
        showing = await showing_dall.get_by_id(showing_id=showing_id)
        if showing is not None:
            return ShowingShow(
                title=showing.title,
                start=showing.start,
                end=showing.end,
                hall_id=showing.hall_id,
                movie_id=showing.movie_id,
                is_active=showing.is_active,
                created_at=showing.created_at,
                updated_at=showing.updated_at,
            )


async def _get_all(session) -> Union[AllShowingsShow, None]:
    async with session.begin():
        showing_dal = ShowingDAL(session)
        showings = await showing_dal.get_all_active()
        showings_show = []
        if showings is not None:
            for showing in showings:
                showings_show.append(
                    ShowingShow(
                        title=showing.title,
                        start=showing.start,
                        end=showing.end,
                        hall_id=showing.hall_id,
                        movie_id=showing.movie_id,
                        is_active=showing.is_active,
                        created_at=showing.created_at,
                        updated_at=showing.updated_at,
                    )
                )
            return AllShowingsShow(result=showings_show)
