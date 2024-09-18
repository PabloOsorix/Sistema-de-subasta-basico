from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository
from app.application.events.event_manager import EventManager
from unittest import TestCase
from unittest.mock import MagicMock


class TestEventManager(TestCase):
    
    def setUp(self) -> None:
        self.event_manager = EventManager()
        self.operation_id = "7evvdd20-5cff-4489-a7b8-406586c6858d"
        self.observer = MagicMock()
        self.observer.update.return_value = True
           
           
    def test_suscribe_update_success(self):   
        result = self.event_manager.subscribe("bid_created", self.observer)
        self.assertTrue(result)
        
    def test_notify_update_success(self):
        self.event_manager.subscribe("bid_created", self.observer)
        result = self.event_manager.notify("bid_created", {"operation_id", })
        self.assertTrue(result)
        