import time
import jwt
import os
from fastapi import  Depends
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# Cambia esta clave por una segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_ONE_DAY_IN_MINUTES = 1140



def create_access_token(data: dict):
    to_encode = data.copy()
    expire = time.time() + ACCESS_TOKEN_EXPIRE_ONE_DAY_IN_MINUTES * 60
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("El token ha expirado")
    except jwt.InvalidTokenError:
        raise Exception("El Token es invalido")
