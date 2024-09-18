from unittest import TestCase
from app.core.validators.validators import AmountValidator, LimitDateValidator, InterestRateValidator
from datetime import datetime

class TestAmountValidator(TestCase):
    
    def test_correct_amount(self):
        amount = 100000
        self.assertIsInstance(AmountValidator().validate(amount), int)
        
    def test_negative_amount(self):
        amount = -100000
        with self.assertRaises(ValueError):            
            AmountValidator.validate(amount)


class TestInterestRateValidator(TestCase):
    
    def test_correct_interest_rate(self):
        interest_rate = 6.5
        self.assertIsInstance(InterestRateValidator().validate(interest_rate), float)
        
    def test_negative_interest_rate(self):
        interest_rate = -1
        with self.assertRaises(ValueError):
            InterestRateValidator.validate(interest_rate)
    
    def test_interest_rate_major_to_30_percent(self):
        interest_rate = 30.01
        with self.assertRaises(ValueError):
            InterestRateValidator.validate(interest_rate)
            
class TestLimitDateValidator(TestCase):
    
    def test_correct_date_format(self):
        limit_date = "2025-12-24"
        self.assertIsInstance(LimitDateValidator().validate(limit_date), datetime)
        
    def test_same_day_date(self):
        limit_date = "2024/09/12"
        with self.assertRaises(Exception):
            LimitDateValidator.validate(limit_date)
    
    def test_date_minior_to_current_day(self):
        limit_date = "2024/09/11"
        with self.assertRaises(Exception):
            LimitDateValidator.validate(limit_date)