from app.utils.hasher import check_hashed_data
from app.application.interfaces.user_service import UserService
from app.external.auth.jwt_handler import create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from pydantic import EmailStr
from app.external.auth.exceptions import CredentialsException
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth/login")



def authenticate_user(email: str, password: str, UserService: UserService):
    user_db = UserService.get_user_by_email(email, password=True)
    user = user_db
    if not user:
        return False
    if not check_hashed_data(password, user.hashed_password):
        return False
    return user

def login(email: str, password: str, UserService: UserService):
    user = authenticate_user(email, password, UserService)
    if not user:
        raise ValueError("Email o Contraseña incorrecta, intente nuevamente")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return payload


def verify_user(current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        email: EmailStr = current_user.get("sub")

        if email is None:
            raise CredentialsException()
        return email
    
    except Exception as error:
        raise Exception(f'{error}')


