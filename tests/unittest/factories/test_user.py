from app.core.factories.user_factory import OperatorUserFactory, InvestorUserFactory
from unittest import TestCase


class TestOperatorUserFactory(TestCase):
    def setUp(self):
        self.operator = OperatorUserFactory().create_new_user(username="Ivan", email="ivantestingoperator@klimb.com", password="TestingPassword007")

    def test_operator_type(self):
        self.assertEqual(self.operator.type, "Operator")


class TestInvestorUserFactory(TestCase):
    # Crear una instancia de StandardOperation

    def setUp(self):
        self.investor = InvestorUserFactory().create_new_user(username="Ivan", email="ivantestinginvestor@klimb.com", password="TestingPassword007")

    # Testear valores predeterminados

    def test_investor_type(self):
        self.assertEqual(self.investor.type, "Investor")
        self.assertEqual(self.investor.username, "Ivan")
        self.assertEqual(self.investor.email, "ivantestinginvestor@klimb.com")
        self.assertEqual(self.investor.password, "TestingPassword007")
        
