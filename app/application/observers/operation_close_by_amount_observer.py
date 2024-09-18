from app.application.interfaces.operation_repository import OperationRepositoryBase
from app.application.events.event_manager import EventManagerBase
from app.core.interfaces.observer import ObserverBase


class OperationCloseObserverByAmount(ObserverBase):
    
    _instance = None

    def __new__(cls, operation_repository: OperationRepositoryBase, event_manager: EventManagerBase):
        cls.operation_repository = OperationRepositoryBase
        cls.event_manager = EventManagerBase
        if cls._instance is None:
            cls._instance = super(OperationCloseObserverByAmount, cls).__new__(cls)
            cls._instance.operation_repository = operation_repository
            cls._instance.event_manager = event_manager
        return cls._instance
    
    def update(self, event_type, data):
        if event_type == "bid_created":
            operation_id = data["operation_id"]
            operation = self.operation_repository.get(query={"id": operation_id})

            # Revismos si el monto disponible es 0 o si la fecha límite ya se venció
            if int(operation.available_amount) <= 0 and operation.status != "closed":
                operation.status = "closed"
                self.operation_repository.update(operation)

                # Notificamos el evento de cierre por si existe algun otro evento escuchando.

                self.event_manager.notify("operation_closed", {"operation_id": operation.id})
                return True
            return False