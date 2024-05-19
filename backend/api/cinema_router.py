from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from actions.auth import get_current_user_from_token
from api import models
from core.permissions import check_role
from db.models import User
from db.session import get_db
from actions.cinema import _create, _delete, _get_by_id, _update, _get_all


cinema_router = APIRouter(prefix="/cinema")


@cinema_router.post("/", response_model=models.CinemaShow)
async def create_cinema(
    cinema: models.CinemaCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.CinemaShow:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warn(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create cinemas",
        )
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
    current_user: User = Depends(get_current_user_from_token),
) -> models.CinemaUpdated:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warn(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete cinemas",
        )
    deleted_cinema_id = await _delete(cinema_id, session)
    if deleted_cinema_id is None:
        raise HTTPException(
            status_code=404, detail=f"Cinema with id {cinema_id} not found"
        )
    logging.info("Delete cinema with id: %s", deleted_cinema_id)
    return models.CinemaUpdated(cinema_id=deleted_cinema_id)


@cinema_router.get(
    "/{cinema_id:int}",
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


@cinema_router.get(
    "/all",
    response_model=models.AllCinemasShow,
)
async def get_all_cinemas(
    session: AsyncSession = Depends(get_db),
) -> models.AllCinemasShow:
    cinemas = await _get_all(session=session)
    if cinemas is None:
        logging.warning("Cinemas not found")
        raise HTTPException(status_code=404, detail=f"Cinemas not found")
    logging.info("Fetch all cinemas")
    return cinemas


@cinema_router.patch(
    "/{cinema_id}",
    response_model=models.CinemaUpdated,
)
async def update_cinema_by_id(
    cinema_id: int,
    body: models.CinemaUpdateRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.CinemaUpdated:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warn(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update cinemas",
        )
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
