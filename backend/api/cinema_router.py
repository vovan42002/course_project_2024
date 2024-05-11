from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api import models
from db.session import get_db
from actions.cinema import _create, _delete, _get_by_id, _update


cinema_router = APIRouter(prefix="/cinema")


@cinema_router.post("/", response_model=models.CinemaShow)
async def create_cinema(
    cinema: models.CinemaCreate,
    session: AsyncSession = Depends(get_db),
) -> models.CinemaShow:
    new_cinema = await _create(body=cinema, session=session)
    if new_cinema is None:
        raise HTTPException(
            status_code=404, detail=f"Cinema with name {cinema.name} already exists"
        )
    return new_cinema


@cinema_router.delete(
    "/{cinema_id}",
    response_model=models.CinemaUpdated,
)
async def delete_cinema(
    cinema_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.CinemaUpdated:
    deleted_cinema_id = await _delete(cinema_id, session)
    if deleted_cinema_id is None:
        raise HTTPException(
            status_code=404, detail=f"Cinema with id {cinema_id} not found"
        )
    logging.info("Delete cinema with id: %s", deleted_cinema_id)
    return models.CinemaUpdated(cinema_id=deleted_cinema_id)


@cinema_router.get(
    "/{cinema_id}",
    response_model=models.CinemaShow,
)
async def get_cinema_by_id(
    cinema_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.CinemaShow:
    cinema = await _get_by_id(cinema_id, session)
    if cinema is None:
        logging.warning("Cinema with id %s not found", cinema_id)
        raise HTTPException(
            status_code=404, detail=f"Cinema with id {cinema_id} not found"
        )
    logging.info("Cinema with id %s found", cinema_id)
    return cinema


@cinema_router.patch(
    "/{cinema_id}",
    response_model=models.CinemaUpdated,
)
async def update_cinema_by_id(
    cinema_id: int,
    body: models.CinemaUpdateRequest,
    session: AsyncSession = Depends(get_db),
) -> models.CinemaUpdated:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for cinema update info should be provided",
        )
    cinema = await _get_by_id(cinema_id, session)
    if cinema is None:
        raise HTTPException(
            status_code=404, detail=f"cinema with id {cinema_id} not found"
        )
    updated_cinema_id = await _update(
        updated_cinema_params=body,
        cinema_id=cinema_id,
        session=session,
    )
    logging.info("Cinema with id: %s updated successfully", updated_cinema_id)
    return models.CinemaUpdated(cinema_id=updated_cinema_id)
