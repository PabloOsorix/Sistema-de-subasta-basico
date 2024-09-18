from fastapi import APIRouter, Depends, status
from app.external.api.dependencies import get_json_user_repository
from app.external.data_access.repositories.json_user_repository import JsonUserRepository
from app.external.api.schemas.user import UserInput, UserOutput
from app.core.factories.user_factory import UserFactory
from app.application.interfaces.user_service import UserService, UserCreateDTO
from app.external.api.schemas.user import UserLoginBase
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.external.api.schemas.auth import TokenInput, TokenOut
from app.external.auth.auth_service import login, get_current_user, verify_user
from app.external.auth.exceptions import CredentialsException
from pydantic import EmailStr
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(dependencies=[Depends(get_json_user_repository)],
                   prefix="/user")


@router.post("/register", response_model=UserOutput)
def create_user(new_user: UserInput, user_repository: JsonUserRepository = Depends(get_json_user_repository)):

    try:
        user_service = UserService(user_repository)
        user_dto = UserCreateDTO(**new_user.model_dump())
        print(user_dto)
        user_db = user_service.create_new_user(new_user, UserFactory)
        return user_db

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_409_CONFLICT,
        )


@router.post("/auth/login")
async def access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       user_repository: JsonUserRepository = Depends(get_json_user_repository)):
    try:
        user_service = UserService(user_repository)
        return login(form_data.username, form_data.password, user_service)
    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.get("/me", response_model=UserOutput)
async def get_user_me(user_repository: JsonUserRepository = Depends(get_json_user_repository),
                      current_user: dict = Depends(get_current_user)):

    try:
        email: EmailStr = current_user.get("sub")

        if email is None:
            raise CredentialsException()

        user_service = UserService(user_repository)
        user_db = user_service.get_user_by_email(str(email))
        return user_db

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_409_CONFLICT,
        )
