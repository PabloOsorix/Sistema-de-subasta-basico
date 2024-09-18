from app.core.factories.user_factory import OperatorUserFactory
from app.application.dtos.user import UserCreateDTO
from app.application.mappers.user_mapper import UserMapper
from app.external.data_access.entities.user_json_entity import UserDbBase
from app.core.entities.user import UserBase
from app.core.entities.user  import Operator
from unittest import TestCase


class TestOperatorUserFactory(TestCase):
    def setUp(self):
        self.operator = OperatorUserFactory().create_new_user(username="Ivan", email="ivantestingoperator@klimb.com", password="TestingPassword007")

    def test_model_to_entity_db_mapper(self):
        user_json = UserMapper.to_entity_db(self.operator)
        
        print(user_json.id, user_json.email)
        self.assertIsInstance(user_json, UserDbBase)

"""
    def test_dto_to_entity(self):
        user_dto = UserCreateDTO(id=self.operator.id, username=self.operator.username, email=self.operator.email,
                                password=self.operator.password, create_date=self.operator.create_date)

        user = UserMapper.to_entity(user_dto)
        
        print(user)
        self.assertIsInstance(user, UserBase)
        """