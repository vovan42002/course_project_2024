from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api import models
from db.session import get_db
from actions.showing import _create, _delete, _get_by_id, _update


showing_router = APIRouter(prefix="/showing")


@showing_router.post("/", response_model=models.ShowingShow)
async def create_showing(
    showing: models.ShowingCreate,
    session: AsyncSession = Depends(get_db),
) -> models.ShowingShow:
    new_showing = await _create(body=showing, session=session)
    if new_showing is None:
        raise HTTPException(
            status_code=404, detail=f"Showing with title {showing.title} already exists"
        )
    return new_showing


@showing_router.delete(
    "/{showing_id}",
    response_model=models.ShowingUpdated,
)
async def delete_showing(
    showing_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.ShowingUpdated:
    deleted_showing_id = await _delete(showing_id, session)
    if deleted_showing_id is None:
        raise HTTPException(
            status_code=404, detail=f"Showing with id {showing_id} not found"
        )
    logging.info("Delete showing with id: %s", deleted_showing_id)
    return models.ShowingUpdated(showing_id=deleted_showing_id)


@showing_router.get(
    "/{showing_id}",
    response_model=models.ShowingShow,
)
async def get_showing_by_id(
    showing_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.ShowingShow:
    showing = await _get_by_id(showing_id, session)
    if showing is None:
        logging.warning("showing with id %s not found", showing_id)
        raise HTTPException(
            status_code=404, detail=f"showing with id {showing_id} not found"
        )
    logging.info("showing with id %s found", showing_id)
    return showing


@showing_router.patch(
    "/{showing_id}",
    response_model=models.ShowingUpdated,
)
async def update_showing_by_id(
    showing_id: int,
    body: models.ShowingUpdateRequest,
    session: AsyncSession = Depends(get_db),
) -> models.ShowingUpdated:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for showing update info should be provided",
        )
    showing = await _get_by_id(showing_id, session)
    if showing is None:
        raise HTTPException(
            status_code=404, detail=f"showing with id {showing_id} not found"
        )
    updated_showing_id = await _update(
        updated_showing_params=body,
        showing_id=showing_id,
        session=session,
    )
    logging.info("showing with id: %s updated successfully", updated_showing_id)
    return models.ShowingUpdated(showing_id=updated_showing_id)
