import unittest
from app.core.factories import BidBuilder
from datetime import datetime

class TestBidBuilder(unittest.TestCase):
    # Crear una instancia de StandardOperation
    
    def setUp(self):
        self.bid_builder = BidBuilder()
        
    
    def test_new_bid(self):
        self.bid_builder.set_operation_id(101)
        self.bid_builder.set_user_id(202)
        self.bid_builder.set_amount(5000)
        self.bid_builder.set_interest_rate(5.5)
        new_bid = self.bid_builder.build()
        
        self.assertIsInstance(new_bid.amount, int)
        self.assertIsInstance(new_bid.interest_rate, float)
        self.assertIsInstance(new_bid.create_date, str)
        self.assertIsInstance(new_bid.create_date, str)
        
        print(new_bid.create_date)

