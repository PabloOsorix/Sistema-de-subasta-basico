from app.core.factories.bid_builder import BidBuilder
from app.core.entities.bid import Bid
import unittest
class TestCreateBidCommand(unittest.TestCase):
    
    def setUp(self):
        self.test_user_id = "ebdc15a2-0a4e-44df-98dd-0fe370857d64"
        self.test_operation_id = "e95a85d7-d638-4de0-a342-bf3e788ff735"
        self.bid_amount = 10000
        self.interest_rate = 4.2
        self.bid_builder = BidBuilder()
    
    
    def test_save_repository(self):
        self.bid_builder.set_amount(self.bid_amount)
        self.bid_builder.set_user_id(self.test_user_id)
        self.bid_builder.set_operation_id(self.test_operation_id)
        self.bid_builder.set_interest_rate(self.interest_rate)
        new_bid = self.bid_builder.build()
    
        self.assertIsInstance(new_bid, Bid)
    """
    
class CreateBidCommand(CreateBidCommandBase):
    def __init__(self, operation_id, user_id, investor_id, amount, interest_rate, BidBuilder: BidBuilderBase):
        self.bid = {
            "user_id": user_id,
            "operation_id":operation_id,
            "investor_id":investor_id,
            "amount": amount,
            "interest_rate":interest_rate
            }
        self.BidBuilder = BidBuilder


    def execute(self):

        # Al ejecutar el comando, notificamos a los observadores
        EventManager.notify("bid_created", self.bid)
        return new_bid

    """