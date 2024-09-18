from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status

class CredentialsException(HTTPException):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                 headers={"WWW-Authenticate": "Bearer"}) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=detail)
