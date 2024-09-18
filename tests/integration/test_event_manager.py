from app.application.events.event_manager import EventManager
from app.application.observers.operation_observer import OperationNewBidObserver
from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository

from app.core.factories.bid_builder import BidBuilder
from unittest import TestCase


class TestEventManager(TestCase):
    
    def setUp(self) -> None:
        self.operation_repository = JsonOperationRepository()
        self.operation_id = "e95a85d7-d638-4de0-a342-bf3e788ff735"
        self.operation = self.operation_repository.get({"id": self.operation_id})
        self.user_id = "7c6f9dfc-cba0-4cf2-9828-0517354ae07c"
        
        self.offered_interest_rate = 4.2
        self.bid_amount = 20000
        self.bid_builder = BidBuilder()
        self.operation_interest_rate = 4.5,
        self.event_manager = self.set_event_manager()
    
    
    def set_event_manager(self):
        event_manager = EventManager()
        operation_observer = OperationNewBidObserver(self.operation_repository)
        event_manager.subscribe("bid_created", operation_observer)
        return event_manager
        
           
    def test_bid_created_success(self):
        data = {"operation_id": self.operation_id, "amount": self.bid_amount}
        result = self.event_manager.notify("bid_created", data=data)
        updated_operation = self.operation_repository.get({"id": self.operation_id})
        
        
        #Verifica que el envio de la notificacion se realizo adecuadamente
        self.assertTrue(result)
        #Verifica que la actualizacion haya sido realizada.
        self.assertNotEqual(updated_operation.available_amount, self.operation.available_amount)
        