from pydantic import BaseModel

class BidCreateDTO(BaseModel):
    operation_id: str
    user_id: str
    amount: int
    interest_rate: float


class BidResponseDTO(BaseModel):
    id: str
    operation_id: str
    amount: int
    interest_rate: float
    create_date: str
