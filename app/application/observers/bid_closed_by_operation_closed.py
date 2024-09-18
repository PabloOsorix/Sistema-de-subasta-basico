from app.application.interfaces.bid_repository import BidRepositoryBase
from app.application.events.event_manager import EventManager
from app.core.interfaces.observer import ObserverBase


class BidClosedByOperationClosedObserver(ObserverBase):
    
    _instance = None

    def __new__(cls, bid_repository: BidRepositoryBase):
        cls.bid_repository = BidRepositoryBase
        if cls._instance is None:
            cls._instance = super(BidClosedByOperationClosedObserver, cls).__new__(cls)
            cls._instance.bid_repository = bid_repository
        return cls._instance
    
    def update(self, event_type, data):
        if event_type == "operation_closed":
            operation_id = data["operation_id"]
            bids = self.bid_repository.get(query={"operation_id": operation_id})
            
            if isinstance(bids, list):
                for bid in bids:
                    print(bid.status)
                    bid.status = "closed"
                    print(bid.status)
                    self.bid_repository.update(bid)
                    # Notificamos el evento de cierre por si existe algun otro evento escuchando.
                    EventManager._instance.notify("bid_closed", {"bid_id": bid.id})
            else:
                bids.status = "closed"
                self.bid_repository.update(bid)
                EventManager._instance.notify("bid_closed", {"bid_id": bids.id})
            
