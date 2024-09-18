from app.application.interfaces.operation_repository import OperationRepositoryBase
from app.application.interfaces.event_manager import EventManagerBase
from datetime import datetime, date


class OperationDeadlineChecker:
    """
    Verifica y cierra las operaciones que han alcanzado su fecha límite o cuyo monto disponible es cero.
    """
    def __init__(self, operation_repository: OperationRepositoryBase, event_manager: EventManagerBase):
        """
        Inicializa el verificador de fechas límite con el repositorio de operaciones.

        Args:
            operation_repository (OperationRepositoryBase): Repositorio de operaciones.
            event_manager (EventManagerBase): Manejador de eventos
        """
        self.operation_repository = operation_repository
        self.event_manager = event_manager

    async def check_and_close_operations(self):
        """
        Funcion asyncrona que verifica las operaciones abiertas y las cierra
        si han alcanzado la fecha límite o si su monto disponible es cero.

        Raises:
            ValueError: Si ocurre un error en el proceso de verificación o actualización.
        """
        operations = self.operation_repository.get(query={"status": "open"})
        
        if not isinstance(operations, list):
            #Aqui podriamos usar un logger que lance una alerta avisando que no se encuentran operaciones abiertas
            return
        
        for operation in operations:
            limit_date = datetime.strptime(operation.limit_date, "%Y-%m-%d")
            if limit_date.date() <= datetime.now().date() or float(operation.amount) <= 0:
                operation.status = "closed"
                self.operation_repository.update(operation)

                self.event_manager.notify("operation_closed", {"operation_id": operation.id})


