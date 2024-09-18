from app.core.interfaces.operations import OperationBase, OperationBaseFactory
from app.core.validators.validators import AmountValidator, InterestRateValidator, LimitDateValidator
from uuid import uuid4
from datetime import datetime

class StandardOperation(OperationBase):
   """
   Representa una operación estándar en el sistema.

   Esta clase hereda de OperationBase y proporciona una implementación
   específica para las operaciones estándar.

   Attributes:
       _id (str): Identificador único de la operación.
       _user_id (str): Identificador del usuario asociado a la operación.
       _description (str): Descripción de la operación.
       _amount (float): Monto total de la operación.
       _available_amount (float): Monto disponible de la operación.
       _interest_rate (float): Tasa de interés de la operación.
       _limit_date (str): Fecha límite de la operación.
       _status (str): Estado actual de la operación.
       _create_date (str): Fecha y hora de creación de la operación.
       _type (str): Tipo de operación, en este caso 'StandardOperation'.
   """

   def __init__(self, user_id: str, description: str, amount: float, available_amount: float, 
                interest_rate: float, limit_date: str) -> None:
       """
       Inicializa una nueva instancia de StandardOperation.

       Args:
           user_id (str): Identificador del usuario asociado a la operación.
           description (str): Descripción de la operación.
           amount (float): Monto total de la operación.
           available_amount (float): Monto disponible de la operación.
           interest_rate (float): Tasa de interés de la operación.
           limit_date (str): Fecha límite de la operación.

       Raises:
           ValueError: Si alguno de los parámetros no cumple con las validaciones.
       """
       AmountValidator.validate(amount)
       InterestRateValidator.validate(interest_rate)
       LimitDateValidator.validate(limit_date)
       
       self._id = str(uuid4())
       self._user_id = user_id
       self._description = description
       self._amount = amount
       self._available_amount = available_amount
       self._interest_rate = interest_rate
       self._limit_date = limit_date
       self._status = "open"
       self._create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       self._type = self.__class__.__name__.__str__()

   @property
   def id(self) -> str:
       """str: El identificador único de la operación."""
       return self._id
   
   @property
   def user_id(self) -> str:
       """str: El identificador del usuario asociado a la operación."""
       return self._user_id
   
   @property
   def description(self) -> str:
       """str: La descripción de la operación."""
       return self._description
   
   @property
   def amount(self) -> float:
       """float: El monto total de la operación."""
       return self._amount
   
   @property
   def available_amount(self) -> float:
       """float: El monto disponible de la operación."""
       return self._available_amount

   @property
   def interest_rate(self) -> float:
       """float: La tasa de interés de la operación."""
       return self._interest_rate

   @property
   def limit_date(self) -> str:
       """str: La fecha límite de la operación."""
       return self._limit_date
   
   @property
   def status(self) -> str:
       """str: El estado actual de la operación."""
       return self._status
   
   @property
   def create_date(self) -> str:
       """str: La fecha y hora de creación de la operación."""
       return self._create_date
   
   @property
   def type(self) -> str:
       """str: El tipo de operación, en este caso 'StandardOperation'."""
       return self._type

