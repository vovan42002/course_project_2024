from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from api import models
from db.session import get_db
from actions.book import _create, _delete, _get_by_id, _update


book_router = APIRouter(prefix="/book")


@book_router.post("/", response_model=models.BookShow)
async def create_book(
    book: models.BookCreate,
    session: AsyncSession = Depends(get_db),
) -> models.BookShow:
    new_book = await _create(body=book, session=session)
    if new_book is None:
        raise HTTPException(
            status_code=404, detail=f"Book with name {book.name} already exists"
        )
    return new_book


@book_router.delete(
    "/{book_id}",
    response_model=models.BookUpdated,
)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_db),
) -> models.BookUpdated:
    deleted_book_id = await _delete(book_id, session)
    if deleted_book_id is None:
        raise HTTPException(status_code=404, detail=f"book with id {book_id} not found")
    logging.info("Delete book with id: %s", deleted_book_id)
    return models.BookUpdated(book_id=deleted_book_id)


@book_router.get(
    "/{book_id}",
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


@book_router.patch(
    "/{book_id}",
    response_model=models.BookUpdated,
)
async def update_book_by_id(
    book_id: int,
    body: models.BookUpdateRequest,
    session: AsyncSession = Depends(get_db),
) -> models.BookUpdated:
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
