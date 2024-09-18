import unittest
from app.application.interfaces.bid_service import BidService, BidCreateDTO, BidResponseDTO
from app.application.events.event_manager import EventManager
from app.application.observers.operation_observer import OperationNewBidObserver
from app.core.factories.bid_builder import BidBuilder
from unittest import TestCase
from unittest.mock import patch, MagicMock
from datetime import datetime


class TestBidService(TestCase):

    def setUp(self):
        # Mocks de los repositorios y el builder
        self.bid_repository = MagicMock()
        self.user_repository = MagicMock()
        self.operation_repository = MagicMock()
        self.event_manager = MagicMock()
        self.bid_builder = MagicMock()
        
        # IDs y datos de prueba
        self.operation_id = "e95a85d7-d638-4de0-a342-bf3e788ff735"
        self.investor_user_id = "7c6f9dfc-cba0-4cf2-9828-0517354ae07c"
        
        # Mock para la operación (puedes modificar según los atributos de la operación)
        self.operation = MagicMock()
        self.operation.id = self.operation_id
        self.operation.status = "open"
        self.operation.available_amount = 50000
        self.operation.interest_rate = 5.0
        
        
        # Mock del user
        self.user = MagicMock()
        self.user.id = "7c6f9dfc-cba0-4cf2-9828-0517354ae07c"
        self.user.type = "Investor"
        
        # Configurar mocks para los métodos que son usados en el servicio
        self.operation_repository.get.return_value = self.operation
        self.user_repository.get_user_by_id.return_value = self.user
        self.event_manager.notify.return_value = True

        
        # Instanciar el servicio con los mocks

        
        # Crear un DTO de prueba para la oferta
        self.test_bid = BidCreateDTO(
            operation_id=str(self.operation_id),
            user_id=self.investor_user_id,
            amount=20000,
            interest_rate=4.2
        )
        
                #Mock para la operacion creada y guardada en db, usada para el retorno del builder
        self.bid_created = MagicMock()
        self.bid_created.id = "98c5a61e-524c-4aa4-ac43-493d85ddbffe"
        self.bid_created.operation_id = self.test_bid.operation_id
        self.bid_created.user_id = self.test_bid.user_id
        self.bid_created.amount = self.test_bid.amount
        self.bid_created.interest_rate = self.test_bid.interest_rate
        self.bid_created.create_date = datetime.now().strftime("%Y-%m-%d")

        # Configurar el mock del builder
        self.bid_builder.build.return_value = self.bid_created
        
        # Mock del event manager

    def _create_bid_service(self):
            self.bid_service = BidService(
            bid_repository=self.bid_repository,
            user_repository=self.user_repository,
            operation_repository=self.operation_repository,
            event_manager=self.event_manager
        )
    
    def test_create_bid(self):
        
        self._create_bid_service()
        # Llamar a create_bid
        created_bid = self.bid_service.create_bid(self.test_bid, self.bid_builder)

        # Verificar que se retornó el tipo correcto
        self.assertIsInstance(created_bid, BidResponseDTO)
        
        
        # Asegurar que los métodos relevantes fueron llamados correctamente
        self.user_repository.get_user_by_id.assert_called_once_with(self.test_bid.user_id)
        self.operation_repository.get.assert_called_once_with(query={"id": self.test_bid.operation_id})
        self.bid_builder.set_user_id.assert_called_once_with(self.user.id)
        self.bid_builder.set_amount.assert_called_once_with(self.test_bid.amount)
        self.bid_builder.set_interest_rate.assert_called_once_with(self.test_bid.interest_rate)
        self.bid_builder.set_operation_id.assert_called_once_with(self.test_bid.operation_id)
        self.event_manager.notify.assert_called_once_with("bid_created", {"operation_id": self.test_bid.operation_id, "amount": self.test_bid.amount})


    def test_create_bid_with_higher_interes_rate(self):
        test_wrong_bid_interes_raate = BidCreateDTO(
            operation_id=str(self.operation_id),
            user_id=self.investor_user_id,
            amount=20000,
            interest_rate=6.0
        )
        self._create_bid_service()
        with self.assertRaises(ValueError):
            created_bid = self.bid_service.create_bid(test_wrong_bid_interes_raate, self.bid_builder)
        
        self.user_repository.get_user_by_id.assert_called_once_with(test_wrong_bid_interes_raate.user_id)
        self.operation_repository.get.assert_called_once_with(query={"id": test_wrong_bid_interes_raate.operation_id})


    def test_create_bid_with_major_available_amount(self):
        test_wrong_bid_major_amount = BidCreateDTO(
            operation_id=str(self.operation_id),
            user_id=self.investor_user_id,
            amount=50999,
            interest_rate=3.2
        )
        self._create_bid_service()
        with self.assertRaises(ValueError):
            self.bid_service.create_bid(test_wrong_bid_major_amount, self.bid_builder)
        
        self.user_repository.get_user_by_id.assert_called_once_with(test_wrong_bid_major_amount.user_id)
        self.operation_repository.get.assert_called_once_with(query={"id": test_wrong_bid_major_amount.operation_id})

    def test_create_bid_for_closed_operation_error(self):
        self.operation.status = "closed"
        #Crea el servicio con el estado de la operacion actualizado
        self._create_bid_service() 
        
        test_wrong_bid_with_closed_operation_id = BidCreateDTO(
            operation_id=str(self.operation_id),
            user_id=self.investor_user_id,
            amount=25000,
            interest_rate=3.2
        )
        with self.assertRaises(ValueError):
            self.bid_service.create_bid(test_wrong_bid_with_closed_operation_id, self.bid_builder)
        
        self.user_repository.get_user_by_id.assert_called_once_with(test_wrong_bid_with_closed_operation_id.user_id)
        self.operation_repository.get.assert_called_once_with(query={"id": test_wrong_bid_with_closed_operation_id.operation_id})
        
        
    def test_create_bid_error_user_not_found(self):
        
        self.user_repository.get_user_by_id.return_value = False
        #Crea el servicio con el id del usuario en respositorio users actualizado
        self._create_bid_service() 
        
        test_wrong_bid_with_closed_operation_id = BidCreateDTO(
            operation_id=str(self.operation_id),
            user_id=self.investor_user_id,
            amount=25000,
            interest_rate=3.2
        )
        with self.assertRaises(ValueError):
            self.bid_service.create_bid(self.test_bid, self.bid_builder)
        
        self.user_repository.get_user_by_id.assert_called_once_with(self.user.id)
        
    
    def test_create_bid_error_user_of_invalid_type(self):
        self.user.type = "Operator"
        
        #self.user_repository.get_user_by_id.return_value = self.user
        #Crea el servicio con el id del usuario en respositorio users actualizado
        self._create_bid_service() 
        with self.assertRaises(ValueError):
            self.bid_service.create_bid(self.test_bid, self.bid_builder)
        
        self.user_repository.get_user_by_id.assert_called_once_with(self.user.id)