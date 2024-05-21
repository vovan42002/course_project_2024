from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from actions.auth import get_current_user_from_token
from api import models
from core.permissions import check_role
from db.models import User
from db.session import get_db
from actions.hall import _create, _delete, _get_all, _get_by_id, _update


hall_router = APIRouter(prefix="/hall")


@hall_router.post("/", response_model=models.HallShow)
async def create_hall(
    hall: models.HallCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.HallShow:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create halls",
        )
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
    current_user: User = Depends(get_current_user_from_token),
) -> models.HallUpdated:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create halls",
        )
    deleted_hall_id = await _delete(hall_id, session)
    if deleted_hall_id is None:
        raise HTTPException(status_code=404, detail=f"Hall with id {hall_id} not found")
    logging.info("Delete hall with id: %s", deleted_hall_id)
    return models.HallUpdated(hall_id=deleted_hall_id)


@hall_router.get(
    "/{hall_id:int}",
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


@hall_router.get(
    "/all",
    response_model=models.AllHallsShow,
)
async def get_all_halls(
    session: AsyncSession = Depends(get_db),
) -> models.AllHallsShow:
    halls = await _get_all(session=session)
    if halls is None:
        logging.warning("Halls not found")
        raise HTTPException(status_code=404, detail="Halls not found")
    logging.info("Fetch all halls")
    return halls


@hall_router.patch(
    "/{hall_id}",
    response_model=models.HallUpdated,
)
async def update_hall_by_id(
    hall_id: int,
    body: models.HallUpdateRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.HallUpdated:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can update halls",
        )
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
