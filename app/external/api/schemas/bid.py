from pydantic import BaseModel, Field
from datetime import datetime


from pydantic import BaseModel


class BidBase(BaseModel):
    operation_id: str
    amount: int
    interest_rate: float


class BidInput(BidBase):
    user_id: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "operation_id": "bf874462-2ac1-4a98-bcae-ca92ac5e4861",
                    "user_id": "dbef75c2-0966-4f5f-8824-55f4836ce179",
                    "amount": "100000",
                    "interest_rate": "5.2",
                    "limit_date": "YYYY-MM-DD"
                }
            ]
        }
    }

class BidOut(BidBase):
    id: str
    create_date: str
