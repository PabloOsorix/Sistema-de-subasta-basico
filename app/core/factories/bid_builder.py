from app.core.interfaces.bid import BidBuilderBase
from app.application.events.event_manager import EventManager
from app.core.entities.bid import Bid




class BidBuilder(BidBuilderBase):
    def __init__(self):
        """
        Clase contructora de objetos bid, esta disenada con el patron Build
        """
        self._operation_id = None
        self._user_id = None
        self._amount = 0
        self._interest_rate = 0.0

    def set_operation_id(self, operation_id):
        self._operation_id = operation_id

    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_amount(self, amount):
        self._amount = amount

    def set_interest_rate(self, interest_rate):
        self._interest_rate = interest_rate

    def build(self):

        if self._operation_id is None:
            raise ValueError("El ID de la operación no puede ser nulo.")
        if self._user_id is None:
            raise ValueError("El ID del inversor no puede ser nulo.")
        if self._amount is None:
            raise ValueError("El monto de la operacion no puede ser nulo")
        if self._interest_rate is None:
            raise ValueError("La tasa de interes no puede ser nula")

        return Bid(
            operation_id=self._operation_id,
            user_id=self._user_id,
            amount=self._amount,
            interest_rate=self._interest_rate
        )
