from typing import Optional

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
