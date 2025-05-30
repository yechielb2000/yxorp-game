import datetime
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from webserver.controllers.user import get_user_controller, UserController
from webserver.models.user import User
from webserver.settings import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        controller: UserController = Depends(get_user_controller),
) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")

    user_id = int(payload.get("sub"))
    user = await controller.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
