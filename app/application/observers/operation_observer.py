from app.core.interfaces.observer import ObserverBase
from app.application.interfaces.operation_repository import OperationRepositoryBase

from datetime import datetime


class OperationNewBidObserver(ObserverBase):
    """
    Observa la creación de una nueva oferta (bid) y actualiza el
    monto disponible de la operación relacionada.
    """
    _instance = None

    def __new__(cls, operation_repository: OperationRepositoryBase):
        """
        Inicializa una nueva instancia de OperationNewBidObserver, asegurándose de que sea un singleton.

        Args:
            operation_repository (OperationRepositoryBase): Repositorio de operaciones para actualizar el monto disponible.

        Returns:
            OperationNewBidObserver: Instancia única de la clase.
        """
        cls.operation_repository = OperationRepositoryBase
        if cls._instance is None:
            cls._instance = super(OperationNewBidObserver, cls).__new__(cls)
            cls._instance.operation_repository = operation_repository
        return cls._instance
    
    def update(self, event_type, data):
        """
        Actualiza el monto disponible de la operación cuando se crea una nueva oferta.

        Args:
            event_type (str): El tipo de evento, debe ser 'bid_created'.
            data (dict): Los datos del evento, que incluyen el 'operation_id' y la cantidad ofertada ('amount').

        Returns:
            bool: Retorna el resultado de la actualización del monto disponible en la operación.
        """
        if event_type == "bid_created":
            self.operation_id = data.get("operation_id")
            self.bid_amount = data.get("amount")

            # Aquí se actualiza el monto disponible
            return self.operation_repository.update_available_amount(self.operation_id, self.bid_amount)



