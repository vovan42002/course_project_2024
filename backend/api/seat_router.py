from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api import models
from db.session import get_db
from actions.seat import _create, _delete, _get_by_id, _update, _get_all
from core.permissions import check_role
from db.models import User
from actions.auth import get_current_user_from_token


seat_router = APIRouter(prefix="/seat")


@seat_router.post("/", response_model=models.SeatShow)
async def create_seat(
    seat: models.SeatCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.SeatShow:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can create seats",
        )
    new_seat = await _create(body=seat, session=session)
    if new_seat is None:
        raise HTTPException(
            status_code=404, detail=f"Seat number {seat.number} already exists"
        )
    return new_seat


@seat_router.delete(
    "/{seat_id}",
    response_model=models.SeatUpdated,
)
async def delete_seat(
    seat_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.SeatUpdated:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete seats",
        )
    deleted_seat_id = await _delete(seat_id, session)
    if deleted_seat_id is None:
        raise HTTPException(status_code=404, detail=f"seat with id {seat_id} not found")
    logging.info("Delete seat with id: %s", deleted_seat_id)
    return models.SeatUpdated(seat_id=deleted_seat_id)


@seat_router.get(
    "/{seat_id:int}",
    response_model=models.SeatShow,
)
async def get_seat_by_id(
    seat_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.SeatShow:
    seat = await _get_by_id(seat_id, session)
    if seat is None:
        logging.warning("Seat with id %s not found", seat_id)
        raise HTTPException(status_code=404, detail=f"Seat with id {seat_id} not found")
    logging.info("Seat with id %s found", seat_id)
    return seat


@seat_router.get(
    "/all",
    response_model=models.AllSeatsShow,
)
async def get_all_halls(
    session: AsyncSession = Depends(get_db),
) -> models.AllSeatsShow:
    seats = await _get_all(session=session)
    if seats is None:
        logging.warning("seats not found")
        raise HTTPException(status_code=404, detail="seats not found")
    logging.info("Fetch all seats")
    return seats


@seat_router.patch(
    "/{seat_id}",
    response_model=models.SeatUpdated,
)
async def update_seat_by_id(
    seat_id: int,
    body: models.SeatUpdateRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.SeatUpdated:
    if not check_role(allowed_roles=["admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete seats",
        )
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for seat update info should be provided",
        )
    seat = await _get_by_id(seat_id, session)
    if seat is None:
        raise HTTPException(status_code=404, detail=f"seat with id {seat_id} not found")
    updated_seat_id = await _update(
        updated_seat_params=body,
        seat_id=seat_id,
        session=session,
    )
    logging.info("Seat with id: %s updated successfully", updated_seat_id)
    return models.SeatUpdated(seat_id=updated_seat_id)
