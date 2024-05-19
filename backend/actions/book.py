from typing import Union

from api.models import AllUserBooksShow, BookCreate, BookShow
from db.dals import BookDAL


async def _create(body: BookCreate, session) -> Union[BookShow, None]:
    async with session.begin():
        book_dal = BookDAL(session)
        book = await book_dal.create(
            seat_id=body.seat_id,
            user_id=body.user_id,
            showing_id=body.showing_id,
        )
        if book is not None:
            return BookShow(
                seat_id=book.seat_id,
                user_id=book.user_id,
                showing_id=book.showing_id,
                created_at=book.created_at,
                updated_at=book.updated_at,
            )


async def _delete(book_id, session) -> Union[int, None]:
    async with session.begin():
        book_dal = BookDAL(session)
        deleted_book = await book_dal.delete(book_id=book_id)
        return deleted_book


async def _update(updated_book_params: dict, book_id: int, session) -> Union[int, None]:
    async with session.begin():
        book_dal = BookDAL(session)
        updated_book = await book_dal.update(book_id, **updated_book_params.dict())
        return updated_book


async def _get_by_id(book_id, session) -> Union[BookShow, None]:
    async with session.begin():
        book_dal = BookDAL(session)
        book = await book_dal.get_by_id(book_id=book_id)
        if book is not None:
            return BookShow(
                seat_id=book.seat_id,
                user_id=book.user_id,
                showing_id=book.showing_id,
                created_at=book.created_at,
                updated_at=book.updated_at,
            )


async def _get_all_by_user_id(user_id, session) -> Union[AllUserBooksShow, None]:
    async with session.begin():
        book_dal = BookDAL(session)
        books = await book_dal.get_by_user_id(user_id=user_id)
        books_show = []
        if books is not None:
            for book in books:
                books_show.append(
                    BookShow(
                        seat_id=book.seat_id,
                        user_id=book.user_id,
                        showing_id=book.showing_id,
                        created_at=book.created_at,
                        updated_at=book.updated_at,
                    )
                )
            return AllUserBooksShow(result=books_show)
