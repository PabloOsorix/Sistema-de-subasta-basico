from pydantic import BaseModel, Field
from datetime import datetime


class OperationBase(BaseModel):
    amount: int
    interest_rate: float
    limit_date: str = Field(default="2024-10-25", examples=["2024/11/12"], description=
                        "Fecha limite para generar una oferta antes de que la operacion cierre.\
                        La fecha no puede ser igual al mismo día o un día anterior. \
                        El formato de la API es YYYY-MM-DD, los guiones son obligatorios"
                    )



class OperationInput(OperationBase):
    user_id: str
    limit_date: str
    description: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "amount": "100000",
                    "interest_rate": "5.2",
                    "limit_date": "YYYY-MM-DD",
                    "description": "inversion en startup xy que esta apliando su sede...",
                    "user_id": "38u8921u49832fdjsa32412"
                }
            ]
        }
    }


class OperationOut(OperationBase):
    id: str
    status: str
    limit_date: str = Field(default="", examples=[""])



    
class OperationOutDetail(OperationOut):
    description: str
    available_amount: int
    create_date: str
    type: str
