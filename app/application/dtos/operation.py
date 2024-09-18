from pydantic import BaseModel

class OperationCreateDTO(BaseModel):
    user_id: str
    amount: int
    description: str
    available_amount: int | str
    interest_rate: float
    limit_date: str

class OperationResponseDTO(BaseModel):
    id: str
    user_id: str
    amount: int
    description: str
    #Tome esta decision ya que el estimado de ofertas por operacion
    #no sera demasiado alto, podemos calcular y enviar el monto disponible
    #para que no deba realizarse desde el front-end el calculo.
    available_amount: int | str
    interest_rate: float
    limit_date: str
    status: str
    create_date: str
    type: str