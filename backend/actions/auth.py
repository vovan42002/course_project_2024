from typing import Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import config
from api.models import ShowUser
from db.dals import UserDAL
from db.models import User
from db.session import get_db
from core.hashing import Hasher


async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(email=email)


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> Union[User, None]:
    user = await _get_user_by_email_for_auth(email=email, session=session)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{config.API_VERSION}/token")


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
) -> ShowUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("email")
        user_id: int = payload.get("user_id")
        if (email or user_id) is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, session=session)
    if user is None:
        raise credentials_exception
    return ShowUser(
        user_id=user.id,
        email=user.email,
        is_active=user.is_active,
    )
