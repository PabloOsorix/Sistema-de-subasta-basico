from unittest import TestCase
from app.core.factories.operation_factory import StandardOperationFactory
from app.core.entities.operation import StandardOperation


class TestStandardOperationFactory(TestCase):
    # Crear una instancia de StandardOperation
    
    def setUp(self):
        pass
        


    def test_standard_operation_setters(self):
        # Crear una instancia de StandardOperation
        self.operation = StandardOperationFactory().new_operation(
            user_id="ebe9fab6-a953-457d-85a0-7284032b0468",
            description="cool_description",
            amount=90000,
            available_amount=90000,
            interest_rate=5.5,
            limit_date="2024-11-09"
        )
        
        # Probar setters
        self.assertIsInstance(self.operation, StandardOperation)
        self.assertIsInstance(self.operation.id, str)
        self.assertIsInstance(self.operation.user_id, str)
        self.assertIsInstance(self.operation.amount, int)
        self.assertIsInstance(self.operation.description, str)
        self.assertIsInstance(self.operation.available_amount, int)
        self.assertIsInstance(self.operation.interest_rate, float)
        self.assertIsInstance(self.operation.limit_date, str)
        
    def test_standard_operation_with_old_limit_date_error(self):
        
        with self.assertRaises(Exception):
            self.operation = StandardOperationFactory().new_operation(
                user_id="ebe9fab6-a953-457d-85a0-7284032b0468",
                description="cool_description",
                amount=90000,
                available_amount=90000,
                interest_rate=5.5,
                limit_date="2024-05-09"
            )
    
    def test_standard_operation_with_limit_date_format(self):
        with self.assertRaises(Exception):
            self.operation = StandardOperationFactory().new_operation(
                user_id="ebe9fab6-a953-457d-85a0-7284032b0468",
                description="cool_description",
                amount=90000,
                available_amount=90000,
                interest_rate=5.5,
                limit_date="-05-09-2024"
            )
    def test_standard_operation_high_interest_rate_error(self):
        with self.assertRaises(Exception):
            self.operation = StandardOperationFactory().new_operation(
                user_id="ebe9fab6-a953-457d-85a0-7284032b0468",
                description="cool_description",
                amount=90000,
                available_amount=90000,
                interest_rate=30.01,
                limit_date="-05-09-2024"
            )
    
    def test_standard_operation_negative_amount_error(self):
        with self.assertRaises(Exception):
            self.operation = StandardOperationFactory().new_operation(
                user_id="ebe9fab6-a953-457d-85a0-7284032b0468",
                description="cool_description",
                amount=-100000,
                available_amount=90000,
                interest_rate=30.01,
                limit_date="-05-09-2024"
            )