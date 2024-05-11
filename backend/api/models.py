from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: int
    email: EmailStr
    is_active: bool


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


class MovieUpdateRequest(TunedModel):
    title: Optional[str] = None
    description: Optional[str] = None


class MovieUpdated(TunedModel):
    movie_id: int
