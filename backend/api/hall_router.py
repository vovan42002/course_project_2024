from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api import models
from db.session import get_db
from actions.hall import _create, _delete, _get_by_id, _update


hall_router = APIRouter(prefix="/hall")


@hall_router.post("/", response_model=models.HallShow)
async def create_hall(
    hall: models.HallCreate,
    session: AsyncSession = Depends(get_db),
) -> models.HallShow:
    new_hall = await _create(body=hall, session=session)
    if new_hall is None:
        raise HTTPException(
            status_code=404, detail=f"Hall with name {hall.name} already exists"
        )
    return new_hall


@hall_router.delete(
    "/{hall_id}",
    response_model=models.HallUpdated,
)
async def delete_hall(
    hall_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.HallUpdated:
    deleted_hall_id = await _delete(hall_id, session)
    if deleted_hall_id is None:
        raise HTTPException(status_code=404, detail=f"Hall with id {hall_id} not found")
    logging.info("Delete hall with id: %s", deleted_hall_id)
    return models.HallUpdated(hall_id=deleted_hall_id)


@hall_router.get(
    "/{hall_id}",
    response_model=models.HallShow,
)
async def get_hall_by_id(
    hall_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.HallShow:
    hall = await _get_by_id(hall_id, session)
    if hall is None:
        logging.warning("Hall with id %s not found", hall_id)
        raise HTTPException(status_code=404, detail=f"Hall with id {hall_id} not found")
    logging.info("Hall with id %s found", hall_id)
    return hall


@hall_router.patch(
    "/{hall_id}",
    response_model=models.HallUpdated,
)
async def update_hall_by_id(
    hall_id: int,
    body: models.HallUpdateRequest,
    session: AsyncSession = Depends(get_db),
) -> models.HallUpdated:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for hall update info should be provided",
        )
    hall = await _get_by_id(hall_id, session)
    if hall is None:
        raise HTTPException(status_code=404, detail=f"Hall with id {hall_id} not found")
    updated_hall_id = await _update(
        updated_hall_params=body,
        hall_id=hall_id,
        session=session,
    )
    logging.info("Hall with id: %s updated successfully", updated_hall_id)
    return models.HallUpdated(hall_id=updated_hall_id)
