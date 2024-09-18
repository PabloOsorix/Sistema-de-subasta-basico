from pydantic import BaseModel, Field
from datetime import datetime


from pydantic import BaseModel


class BidBase(BaseModel):
    operation_id: str
    amount: int
    interest_rate: float


class BidInput(BidBase):
    user_id: str

class BidOut(BidBase):
    id: str
    create_date: str
