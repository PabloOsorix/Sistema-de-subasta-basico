from pydantic import BaseModel, EmailStr
from typing import Literal

class UserBase(BaseModel):
    username: str
    email: EmailStr
    type:  Literal['Operator', 'Investor']



class UserInput(UserBase):
    password: str
    

class UserOutput(UserBase):
    id: str


class UserLoginBase(BaseModel):
    email: EmailStr
    password: str