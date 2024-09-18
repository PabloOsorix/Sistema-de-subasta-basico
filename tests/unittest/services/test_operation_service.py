from app.application.dtos.operation import OperationCreateDTO, OperationResponseDTO
from app.external.data_access.repositories.json_user_repository import JsonUserRepository
from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository
from app.application.interfaces.operation_service import OperationService
from unittest import TestCase
from uuid import uuid4
from unittest.mock import patch, MagicMock
from pydantic import EmailStr


class TestOperationService(TestCase):

    def setUp(self):
        self.user_repository = MagicMock()
        self.operation_repository = MagicMock()
        self.standard_operation_factory = MagicMock()

        self.user_id = "9c522ff5-09d2-4a67-b5f8-224d273c60ff"
        self.user = MagicMock()
        self.user.id = self.user_id
        self.user.type = "Operator"

        self.operation_dto = MagicMock()
        self.operation_dto.user_id = self.user_id
        self.operation_dto.description = "Expansion y crecimiento de startup Wood, que genera ingresos de 10x la inversión que se está subastando"
        self.operation_dto.amount = 85000
        self.operation_dto.available_amount = self.operation_dto.amount
        self.operation_dto.interest_rate = 5.2
        self.operation_dto.limit_date = "2024-11-30"
        self.user_repository.get_user_by_id.return_value = self.user
        
        self.new_operation = MagicMock()
        self.new_operation.id = "ff4d8bbb-65bd-4424-acb3-303696ebe311"
        self.new_operation.user_id = self.user_id
        self.new_operation.description = "Expansion y crecimiento de startup Wood, que genera ingresos de 10x la inversión que se está subastando"
        self.new_operation.amount = 85000
        self.new_operation.available_amount = self.operation_dto.amount
        self.new_operation.interest_rate = 5.2
        self.new_operation.limit_date = "2024-11-30"
        self.new_operation.create_date = "2024-09-15 11:19:17"
        self.new_operation.status="open"
        self.new_operation.type="StandardOperation"
        
        self.standard_operation_factory.new_operation.return_value = self.new_operation

    def _create_operation_service(self):
        self.operation_service = OperationService(self.operation_repository,
                                                  self.user_repository
                                                  )

    
    def test_create_operation(self):
        
        self._create_operation_service()
        # Llamar a create_bid
        new_operation = self.operation_service.create_operation(self.operation_dto, self.standard_operation_factory)

        # Verificar que se retornó el tipo correcto
        self.assertIsInstance(new_operation, OperationResponseDTO)
        
        
        # Asegurar que los métodos relevantes fueron llamados correctamente
        self.user_repository.get_user_by_id.assert_called_once_with(self.operation_dto.user_id)
        self.standard_operation_factory.new_operation.assert_called_once_with(
            user_id=self.operation_dto.user_id,
            description=self.operation_dto.description,
            amount=self.operation_dto.amount,
            available_amount=self.operation_dto.amount,
            interest_rate=self.operation_dto.interest_rate,
            limit_date=self.operation_dto.limit_date
        )
    
    def test_operation_with_higher_interes_rate_error(self):
        self.operation_dto.interest_rate = 31.0
        self._create_operation_service()
        
        with self.assertRaises(ValueError):
            self.operation_service.create_operation(self.operation_dto, self.standard_operation_factory)
        
        
        self.user_repository.get_user_by_id.assert_called_once_with(self.operation_dto.user_id)


    def test_operation_with_higher_interes_rate_error(self):
        self.operation_dto.interest_rate = 31.0
        self._create_operation_service()
        
        with self.assertRaises(ValueError):
            self.operation_service.create_operation(self.operation_dto, self.standard_operation_factory)
        
        
        self.user_repository.get_user_by_id.assert_called_once_with(self.operation_dto.user_id)
        
    def test_operation_with_negative_amount_error(self):
        self.operation_dto.amount = -10000
        self._create_operation_service()
        
        with self.assertRaises(ValueError):
            self.operation_service.create_operation(self.operation_dto, self.standard_operation_factory)
        
        
        self.user_repository.get_user_by_id.assert_called_once_with(self.operation_dto.user_id)
    
    
    def test_oepration_with_invalid_limit_date_format(self):
        self.operation_dto.limit_date = "30-11-2024"
        self._create_operation_service()
        
        with self.assertRaises(Exception):
            self.operation_service.create_operation(self.operation_dto, self.standard_operation_factory)
        
        self.user_repository.get_user_by_id.assert_called_once_with(self.operation_dto.user_id)
    
    def test_oepration_with_today_day_as_limit_date_format(self):
        self.operation_dto.limit_date = "2024-09-2024"
        self._create_operation_service()
        
        with self.assertRaises(Exception):
            self.operation_service.create_operation(self.operation_dto, self.standard_operation_factory)
        
        self.user_repository.get_user_by_id.assert_called_once_with(self.operation_dto.user_id)

