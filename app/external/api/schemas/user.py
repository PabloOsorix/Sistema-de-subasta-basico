from pydantic import BaseModel, EmailStr
from typing import Literal

class UserBase(BaseModel):
    username: str
    email: EmailStr
    type:  Literal['Operator', 'Investor']
    
    
    



class UserInput(UserBase):
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "Fernanda Gonzales",
                    "email": "fernanda01@gmail.com",
                    "type": "Operator || Investor",
                    "password": "fernanda01Investor"
                }
            ]
        }
    }
    

class UserOutput(UserBase):
    id: str


class UserLoginBase(BaseModel):
    email: EmailStr
    password: str