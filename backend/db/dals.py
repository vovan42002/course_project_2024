from sqlalchemy import update, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import datetime

from db.models import User, Cinema, Hall, Movie, Showing, Seat, Book


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        email: str,
        hashed_password: str,
        first_name: str = None,
        last_name: str = None,
    ) -> User:
        try:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                hashed_password=hashed_password,
            )
            self.db_session.add(new_user)
            await self.db_session.flush()
            return new_user
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while creating a user: {str(e)}")
            return None

    async def delete_user(self, user_id: int) -> int:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: int, **kwargs) -> int:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


class CinemaDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        name: str,
        description: str,
    ) -> Cinema:
        try:
            new_cinema = Cinema(name=name, description=description)
            self.db_session.add(new_cinema)
            await self.db_session.flush()
            return new_cinema
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while creating a user: {str(e)}")
            return None

    async def delete(self, cinema_id: int) -> int:
        """
        We shouldn't delete cinema object at all.
        We should mark it as inactive
        """
        query = (
            update(Cinema)
            .where(and_(Cinema.id == cinema_id, Cinema.is_active == True))
            .values(is_active=False)
            .returning(Cinema.id)
        )
        res = await self.db_session.execute(query)
        deactivated_cinema_id_row = res.fetchone()
        if deactivated_cinema_id_row is not None:
            return deactivated_cinema_id_row[0]

    async def get_by_id(self, cinema_id: int) -> Cinema:
        query = select(Cinema).where(Cinema.id == cinema_id)
        res = await self.db_session.execute(query)
        cinema_row = res.fetchone()
        if cinema_row is not None:
            return cinema_row[0]

    async def update(self, cinema_id: int, **kwargs) -> int:
        query = (
            update(Cinema)
            .where(and_(Cinema.id == cinema_id, Cinema.is_active == True))
            .values(kwargs)
            .returning(Cinema.id)
        )
        res = await self.db_session.execute(query)
        update_cinema_id_row = res.fetchone()
        if update_cinema_id_row is not None:
            return update_cinema_id_row[0]


class HallDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        name: str,
        description: str,
        cinema_id: int,
    ) -> Hall:
        try:
            new_hall = Hall(
                name=name,
                description=description,
                cinema_id=cinema_id,
            )
            self.db_session.add(new_hall)
            await self.db_session.flush()
            return new_hall
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while creating a user: {str(e)}")
            return None

    async def delete(self, hall_id: int) -> int:
        """
        We shouldn't delete cinema object at all.
        We should mark it as inactive
        """
        query = (
            update(Hall)
            .where(and_(Hall.id == hall_id, Hall.is_active == True))
            .values(is_active=False)
            .returning(Hall.id)
        )
        res = await self.db_session.execute(query)
        deactivated_hall_id_row = res.fetchone()
        if deactivated_hall_id_row is not None:
            return deactivated_hall_id_row[0]

    async def get_by_id(self, hall_id: int) -> Hall:
        query = select(Hall).where(Hall.id == hall_id)
        res = await self.db_session.execute(query)
        hall_row = res.fetchone()
        if hall_row is not None:
            return hall_row[0]

    async def update(self, hall_id: int, **kwargs) -> int:
        query = (
            update(Hall)
            .where(and_(Hall.id == hall_id, Hall.is_active == True))
            .values(kwargs)
            .returning(Hall.id)
        )
        res = await self.db_session.execute(query)
        updated_hall_id_row = res.fetchone()
        if updated_hall_id_row is not None:
            return updated_hall_id_row[0]


class MovieDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        title: str,
        description: str,
    ) -> Movie:
        try:
            new_movie = Movie(
                title=title,
                description=description,
            )
            self.db_session.add(new_movie)
            await self.db_session.flush()
            return new_movie
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while creating a user: {str(e)}")
            return None

    async def delete(self, movie_id: int) -> int:
        """
        We shouldn't delete cinema object at all.
        We should mark it as inactive
        """
        query = (
            update(Movie)
            .where(and_(Movie.id == movie_id, Movie.is_active == True))
            .values(is_active=False)
            .returning(Movie.id)
        )
        res = await self.db_session.execute(query)
        deactivated_movie_id_row = res.fetchone()
        if deactivated_movie_id_row is not None:
            return deactivated_movie_id_row[0]

    async def get_by_id(self, movie_id: int) -> Movie:
        query = select(Movie).where(Movie.id == movie_id)
        res = await self.db_session.execute(query)
        movie_row = res.fetchone()
        if movie_row is not None:
            return movie_row[0]

    async def update(self, movie_id: int, **kwargs) -> int:
        query = (
            update(Movie)
            .where(and_(Movie.id == movie_id, Movie.is_active == True))
            .values(kwargs)
            .returning(Movie.id)
        )
        res = await self.db_session.execute(query)
        updated_movie_id_row = res.fetchone()
        if updated_movie_id_row is not None:
            return updated_movie_id_row[0]


class ShowingDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        title: str,
        start: datetime,
        end: datetime,
        hall_id: int,
        movie_id: int,
    ) -> Showing:
        try:
            new_showing = Showing(
                title=title,
                start=start,
                end=end,
                hall_id=hall_id,
                movie_id=movie_id,
            )
            self.db_session.add(new_showing)
            await self.db_session.flush()
            return new_showing
        except Exception as e:
            print(f"An error occurred while creating a showing: {str(e)}")
            return None

    async def delete(self, showing_id: int) -> int:
        query = (
            update(Showing)
            .where(and_(Showing.id == showing_id, Showing.is_active == True))
            .values(is_active=False)
            .returning(Showing.id)
        )
        res = await self.db_session.execute(query)
        deactivated_showing_id_row = res.fetchone()
        if deactivated_showing_id_row is not None:
            return deactivated_showing_id_row[0]

    async def get_by_id(self, showing_id: int) -> Showing:
        query = select(Showing).where(Showing.id == showing_id)
        res = await self.db_session.execute(query)
        showing_row = res.fetchone()
        if showing_row is not None:
            return showing_row[0]

    async def update(self, showing_id: int, **kwargs) -> int:
        query = (
            update(Showing)
            .where(and_(Showing.id == showing_id, Showing.is_active == True))
            .values(kwargs)
            .returning(Showing.id)
        )
        res = await self.db_session.execute(query)
        updated_showing_id_row = res.fetchone()
        if updated_showing_id_row is not None:
            return updated_showing_id_row[0]


class SeatDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        number: int,
        hall_id: int,
    ) -> Seat:
        try:
            new_seat = Seat(
                number=number,
                hall_id=hall_id,
            )
            self.db_session.add(new_seat)
            await self.db_session.flush()
            return new_seat
        except Exception as e:
            print(f"An error occurred while creating a seat: {str(e)}")
            return None

    async def delete(self, seat_id: int) -> int:
        query = (
            update(Seat)
            .where(and_(Seat.id == seat_id, Seat.is_active == True))
            .values(is_active=False)
            .returning(Seat.id)
        )
        res = await self.db_session.execute(query)
        deactivated_seat_id_row = res.fetchone()
        if deactivated_seat_id_row is not None:
            return deactivated_seat_id_row[0]

    async def get_by_id(self, seat_id: int) -> Seat:
        query = select(Seat).where(Seat.id == seat_id)
        res = await self.db_session.execute(query)
        seat_row = res.fetchone()
        if seat_row is not None:
            return seat_row[0]

    async def update(self, seat_id: int, **kwargs) -> int:
        query = (
            update(Seat)
            .where(and_(Seat.id == seat_id, Seat.is_active == True))
            .values(kwargs)
            .returning(Seat.id)
        )
        res = await self.db_session.execute(query)
        updated_seat_id_row = res.fetchone()
        if updated_seat_id_row is not None:
            return updated_seat_id_row[0]


class BookDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(
        self,
        seat_id: int,
        user_id: int,
        showing_id: int,
    ) -> Book:
        try:
            new_book = Book(
                seat_id=seat_id,
                user_id=user_id,
                showing_id=showing_id,
            )
            self.db_session.add(new_book)
            await self.db_session.flush()
            return new_book
        except Exception as e:
            print(f"An error occurred while creating a booking: {str(e)}")
            return None

    async def delete(self, book_id: int) -> int:
        query = (
            update(Book)
            .where(Book.id == book_id)
            .values(is_active=False)
            .returning(Book.id)
        )
        res = await self.db_session.execute(query)
        deactivated_book_id_row = res.fetchone()
        if deactivated_book_id_row is not None:
            return deactivated_book_id_row[0]

    async def get_by_id(self, book_id: int) -> Book:
        query = select(Book).where(Book.id == book_id)
        res = await self.db_session.execute(query)
        book_row = res.fetchone()
        if book_row is not None:
            return book_row[0]

    async def update(self, book_id: int, **kwargs) -> int:
        query = update(Book).where(Book.id == book_id).values(kwargs).returning(Book.id)
        res = await self.db_session.execute(query)
        updated_book_id_row = res.fetchone()
        if updated_book_id_row is not None:
            return updated_book_id_row[0]
