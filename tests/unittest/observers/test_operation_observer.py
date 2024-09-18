from app.application.observers.operation_observer import OperationNewBidObserver
from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository
from unittest import TestCase
from unittest.mock import MagicMock

class TestEventManager(TestCase):
    
    def setUp(self) -> None:

        self.operation_repository = MagicMock()
        self.event_type = "bid_created"
        
        # Mockeamos el repositorio de operaciones
        self.operation_repository = MagicMock()
        
        self.operation_id = "ecb9b643-e0fb-4f68-9c94-0edd9b6c17ca"
        
        # Mockeamos la operacion que actualizara el observer.
        self.operation = MagicMock()
        self.operation.id = self.operation_id
        self.operation.available_amount=200000
        
        self.updated_operation = MagicMock()
        self.updated_operation.id = self.operation_id

        # configuramos el retorno de la funcion self.operation_repository.get() dentro del observer
        self.operation_repository.get.return_value = self.operation
        self.operation_repository.update_available_amount.return_value = self.updated_operation
        
        # Configuramos el monto del bid que debeera ser descontado del monto disponible del negocio.
        self.bid_amount = 20000
        
        # Configuramos el retorno de la funcion updated_operation.available_amount
        self.updated_operation.available_amount=self.operation.available_amount - self.bid_amount
    
    
    def _create_observer(self):
        self.operation_observer = OperationNewBidObserver(self.operation_repository)

    def test_observer_update_success(self):
        self._create_observer()
        
        data = {"operation_id": self.operation_id, "amount": self.bid_amount}
        bid_result = self.operation_observer.update(self.event_type, data)
        
        
        #Verifica que el envio de la notificacion se realizo adecuadamente
        self.assertTrue(bid_result)
        self.operation_repository.update_available_amount.assert_called_with(self.operation_id, self.bid_amount)
        #Verifica que la actualizacion haya sido realizada.
        print(bid_result.available_amount)
        self.assertNotEqual(bid_result.available_amount, 200000)
        