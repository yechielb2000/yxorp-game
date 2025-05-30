from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from webserver.controllers.user import get_user_controller, UserController
from webserver.schemas.token import Token
from webserver.utils.jwt_token import create_access_token
from webserver.utils.passwords import verify_password

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/token", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        controller: UserController = Depends(get_user_controller),
):
    user = await controller.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
