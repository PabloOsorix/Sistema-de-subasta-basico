from datetime import datetime
from app.core.interfaces.bid import BidBase
from app.core.validators.validators import AmountValidator, InterestRateValidator
from uuid import uuid4


class Bid(BidBase):
   """
   Representa una oferta (bid) en el sistema.

   Esta clase hereda de BidBase y proporciona una implementación
   específica para las ofertas.

   Attributes:
       _id (str): Identificador único de la oferta.
       _user_id (str): Identificador del usuario que realiza la oferta.
       _operation_id (str): Identificador de la operación asociada.
       _amount (float): Monto de la oferta.
       _interest_rate (float): Tasa de interés propuesta en la oferta.
       _status (str): Estado actual de la oferta.
       _create_date (str): Fecha y hora de creación de la oferta.
       _type (str): Tipo de la oferta, en este caso 'Bid'.
   """

   def __init__(self, user_id: str, operation_id: str, amount: float, interest_rate: float):
       """
       Inicializa una nueva instancia de Bid.

       Args:
           user_id (str): Identificador del usuario que realiza la oferta.
           operation_id (str): Identificador de la operación asociada.
           amount (float): Monto de la oferta.
           interest_rate (float): Tasa de interés propuesta en la oferta.

       Raises:
           ValueError: Si el monto o la tasa de interés no cumplen con las validaciones.
       """
       AmountValidator.validate(amount)
       InterestRateValidator.validate(interest_rate)

       self._id = str(uuid4())
       self._user_id = user_id
       self._operation_id = operation_id
       self._amount = amount
       self._interest_rate = interest_rate
       self._status = "open"
       self._create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       self._type = __class__.__name__.__str__()

   @property
   def id(self) -> str:
       """str: El identificador único de la oferta."""
       return self._id
   
   @property
   def user_id(self) -> str:
       """str: El identificador del usuario que realiza la oferta."""
       return self._user_id

   @property
   def operation_id(self) -> str:
       """str: El identificador de la operación asociada."""
       return self._operation_id

   @property
   def amount(self) -> float:
       """float: El monto de la oferta."""
       return self._amount

   @property
   def interest_rate(self) -> float:
       """float: La tasa de interés propuesta en la oferta."""
       return self._interest_rate

   @property
   def status(self) -> str:
       """str: El estado actual de la oferta."""
       return self._status
   
   @property
   def create_date(self) -> str:
       """str: La fecha y hora de creación de la oferta."""
       return self._create_date

   @property
   def type(self) -> str:
       """str: El tipo de la oferta, en este caso 'Bid'."""
       return self._type
