from pydantic import BaseModel, EmailStr

class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    type: str

class UserResponseDTO(BaseModel):
    id: str
    username: str
    email: str
    type: str
    
    
    