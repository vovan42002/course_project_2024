from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api import models
from db.session import get_db
from actions.book import _create, _delete, _get_by_id, _update, _get_all_by_user_id
from core.permissions import check_role
from actions.auth import get_current_user_from_token
from db.models import User

book_router = APIRouter(prefix="/book")


@book_router.post("/", response_model=models.BookShow)
async def create_book(
    book: models.BookCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.BookShow:
    if not check_role(allowed_roles=["user", "vendor", "admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only user, vendor or admin can create book",
        )
    new_book = await _create(body=book, session=session)
    if new_book is None:
        raise HTTPException(
            status_code=404,
            detail=f"Book for user {book.user_id} seat {book.seat_id} showing {book.showing_id} already exists",
        )
    return new_book


@book_router.delete(
    "/{book_id}",
    response_model=models.BookUpdated,
)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.BookUpdated:
    if not check_role(allowed_roles=["user", "vendor", "admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only user, vendor or admin can delete book",
        )
    deleted_book_id = await _delete(book_id, session)
    if deleted_book_id is None:
        raise HTTPException(status_code=404, detail=f"book with id {book_id} not found")
    logging.info("Delete book with id: %s", deleted_book_id)
    return models.BookUpdated(book_id=deleted_book_id)


@book_router.get(
    "/{book_id:int}",
    response_model=models.BookShow,
)
async def get_book_by_id(
    book_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.BookShow:
    book = await _get_by_id(book_id, session)
    if book is None:
        logging.warning("book with id %s not found", book_id)
        raise HTTPException(status_code=404, detail=f"book with id {book_id} not found")
    logging.info("book with id %s found", book_id)
    return book


@book_router.get(
    "/all/{user_id}",
    response_model=models.AllUserBooksShow,
)
async def get_all_halls(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.AllUserBooksShow:
    books = await _get_all_by_user_id(session=session, user_id=user_id)
    if books is None:
        logging.warninging("books for user %s not found", user_id)
        raise HTTPException(
            status_code=404, detail=f"Books for user {user_id} not found"
        )
    logging.info("Fetch all books")
    return books


@book_router.patch(
    "/{book_id}",
    response_model=models.BookUpdated,
)
async def update_book_by_id(
    book_id: int,
    body: models.BookUpdateRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> models.BookUpdated:
    if not check_role(allowed_roles=["user", "vendor", "admin"], user=current_user):
        logging.warning(
            "User with email %s don't have enough permissions", current_user.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only user, vendor or admin can update book",
        )
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for book update info should be provided",
        )
    book = await _get_by_id(book_id, session)
    if book is None:
        raise HTTPException(status_code=404, detail=f"book with id {book_id} not found")
    updated_book_id = await _update(
        updated_book_params=body,
        book_id=book_id,
        session=session,
    )
    logging.info("book with id: %s updated successfully", updated_book_id)
    return models.BookUpdated(book_id=updated_book_id)
