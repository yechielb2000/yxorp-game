from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from webserver.controllers.user import get_user_controller, UserController
from webserver.schemas.token import Token
from webserver.schemas.user import UserCreate, UserRead
from webserver.utils.jwt_token import create_access_token
from webserver.utils.logger_setup import get_user_logger, get_infra_logger
from webserver.utils.passwords import verify_password

user_router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@user_router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        usr_controller: UserController = Depends(get_user_controller),
):
    get_user_logger().info("User login", extra={"username": form_data.username})
    user = await usr_controller.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        get_user_logger().info("User login failed", extra={"username": form_data.username})
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect username or password")

    get_user_logger().info("User login successful", extra={"username": form_data.username})
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/register", response_model=UserRead)
async def register_user(
        user_data: UserCreate,
        usr_controller: UserController = Depends(get_user_controller),
):
    get_infra_logger().info("Trying to register new user", extra={"username": user_data.username})
    existing_user = await usr_controller.get_user_by_username(user_data.username)
    if existing_user:
        get_user_logger().info("User already exists", extra={"username": user_data.username})
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Username already taken")

    get_infra_logger().info("Creating new user", extra={"username": user_data.username})
    user = await usr_controller.create_user(user_data)
    return user
