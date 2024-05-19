from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: int
    email: EmailStr
    is_active: bool


class ShowUserWithRoles(ShowUser):
    is_superuser: bool
    is_vendor: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class UpdatedUserResponse(BaseModel):
    updated_user_id: int


class UpdatedUserRequest(BaseModel):
    email: Optional[EmailStr]
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class HealthCheckResponse(BaseModel):
    """
    A response model for the health check
    """

    status: str = Field(
        ...,
        title="Status",
        description="A status of the service",
        example="OK",
    )


class CinemaCreate(TunedModel):
    name: str
    description: str


class CinemaShow(BaseModel):
    name: str
    description: str
    is_active: bool
    updated_at: datetime
    created_at: datetime


class AllCinemasShow(BaseModel):
    result: List[CinemaShow]


class CinemaUpdateRequest(TunedModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CinemaUpdated(TunedModel):
    cinema_id: int


class HallCreate(TunedModel):
    name: str
    description: str
    cinema_id: int


class HallShow(BaseModel):
    name: str
    description: str
    is_active: bool
    updated_at: datetime
    created_at: datetime


class AllHallsShow(BaseModel):
    result: List[HallShow]


class HallUpdateRequest(TunedModel):
    name: Optional[str] = None
    description: Optional[str] = None


class HallUpdated(TunedModel):
    hall_id: int


class MovieCreate(TunedModel):
    title: str
    description: str


class MovieShow(BaseModel):
    title: str
    description: str
    is_active: bool
    updated_at: datetime
    created_at: datetime


class AllMoviesShow(BaseModel):
    result: List[MovieShow]


class MovieUpdateRequest(TunedModel):
    title: Optional[str] = None
    description: Optional[str] = None


class MovieUpdated(TunedModel):
    movie_id: int


class ShowingCreate(TunedModel):
    title: str
    start: datetime
    end: datetime
    hall_id: int
    movie_id: int


class ShowingShow(BaseModel):
    title: str
    start: datetime
    end: datetime
    hall_id: int
    movie_id: int
    is_active: bool
    updated_at: datetime
    created_at: datetime


class AllShowingsShow(BaseModel):
    result: List[ShowingShow]


class ShowingUpdateRequest(TunedModel):
    title: Optional[str] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class ShowingUpdated(TunedModel):
    showing_id: int


class SeatCreate(TunedModel):
    number: int
    hall_id: int


class SeatShow(BaseModel):
    number: int
    hall_id: int
    is_active: bool
    updated_at: datetime
    created_at: datetime


class AllSeatsShow(BaseModel):
    result: List[SeatShow]


class SeatUpdateRequest(TunedModel):
    number: Optional[int] = None
    hall_id: Optional[int] = None


class SeatUpdated(TunedModel):
    seat_id: int


class BookCreate(TunedModel):
    seat_id: int
    user_id: int
    showing_id: int


class BookShow(BaseModel):
    seat_id: int
    user_id: int
    showing_id: int
    updated_at: datetime
    created_at: datetime


class AllUserBooksShow(BaseModel):
    result: List[BookShow]


class BookUpdateRequest(TunedModel):
    seat_id: Optional[int] = None
    user_id: Optional[int] = None
    showing_id: Optional[int] = None


class BookUpdated(TunedModel):
    book_id: int
