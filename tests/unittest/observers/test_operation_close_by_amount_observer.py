from unittest import mock, TestCase

from app.application.events.event_manager import EventManager
from app.application.interfaces.operation_repository import OperationRepositoryBase
from app.external.data_access.entities.operation_json_entity import OperationJsonEntity
from app.core.interfaces.observer import ObserverBase

from app.application.observers.operation_close_by_amount_observer import OperationCloseObserverByAmount
from unittest.mock import patch, MagicMock

class TestOperationCloseObserverByAmount(TestCase):
    
    
    def setUp(self):
        self.operation_repository = MagicMock()
        

        self.operation_id = "7evvdd20-5cff-4489-a7b8-406586c6858d"
        self.operation = MagicMock()
        self.operation.id = self.operation_id
        self.operation.available_amount = "0"
        self.operation.status = "open"
        
        self.updated_operation = MagicMock()
        self.updated_operation.id = self.operation.id
        self.updated_operation.status = "closed"
        
        self.event_manager = MagicMock()
        self.event_manager.notify.return_value = True
        
        self.operation_repository.get.return_value = self.operation
        self.operation_repository.update.return_value = True
        
    def _create_observer(self): 
        self.closing_observer = OperationCloseObserverByAmount(self.operation_repository, self.event_manager)


    def test_close_operation_by_zero_available_amount(self):
        self._create_observer()
        event_data = {"operation_id": self.operation.id}
        result = self.closing_observer.update(event_type="bid_created", data=event_data)

        # Verificar que la operación se marcó como cerrada
        self.operation_repository.get.assert_called_once_with(query={"id": self.operation.id})
        self.operation_repository.update.assert_called_once_with(self.operation)
        self.assertEqual(self.operation.status, "closed")
        self.assertTrue(result)

    def test_try_to_close_closed_operation(self):
        self.operation.status = "closed"
        
        self._create_observer()
        event_data = {"operation_id": self.operation.id}
        
        result = self.closing_observer.update(event_type="bid_created", data=event_data)

        self.assertFalse(result)