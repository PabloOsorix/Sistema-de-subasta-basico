from pydantic import BaseModel

class TokenBase(BaseModel):
    access_token: str
    token_type: str

class TokenInput(BaseModel):
    pass

class TokenOut(TokenBase):
    pass
    
