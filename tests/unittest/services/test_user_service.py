from app.application.interfaces.user_service import UserService, UserCreateDTO, UserResponseDTO
from app.external.data_access.repositories.json_user_repository import JsonUserRepository
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4


class TestUserService(TestCase):

    def setUp(self):
        
        self.user_repository = MagicMock()
        self.user_factory = MagicMock()


        self.user_id = "1306c79b-e90b-4df5-9117-ad9b06bfd3da"
        self.user_dto = MagicMock()
        self.user_dto.username = "Fernanda"
        self.user_dto.email = "fernanda.elegante.01@gmail.com"
        self.user_dto.password = "elegante.fernanda.478324"
        self.user_dto.type = "Operator"

        self.new_operator_user = MagicMock()
        self.new_operator_user.id = self.user_id
        self.new_operator_user.email = self.user_dto.email
        self.new_operator_user.username = self.user_dto.username
        self.new_operator_user.password = "$2b$12$ODGS3v5WsKlUFkr/C84FzOa1H4ItuSAcJH3kYcM8LiDC4eqFzYtGS"
        self.new_operator_user.type="Operator"
        
        self.user_repository.get_user_by_email.return_value = False
        self.user_factory.create_new_user.return_value = self.new_operator_user

    def _create_user_service(self):
        self.user_service = UserService(self.user_repository)

    
    def test_create_operation(self):
        
        self._create_user_service()
        # Llamar a create_bid
        new_operation = self.user_service.create_new_user(self.user_dto, self.user_factory)

        # Verificar que se retornó el tipo correcto
        self.assertIsInstance(new_operation, UserResponseDTO)
        
    
    def test_get_user_by_email(self):
        self.user_repository.get_user_by_email.return_value = self.new_operator_user
        self._create_user_service()
        
        new_user = self.user_service.get_user_by_email(email=self.user_dto.email)
        
        self.assertEqual(new_user.email, self.user_dto.email)
        self.assertIsInstance(new_user, UserResponseDTO)
        
