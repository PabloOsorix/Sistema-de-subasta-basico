from app.core.interfaces.bid import BidBuilderBase
from app.application.interfaces.operation_repository import OperationRepositoryBase
from app.application.interfaces.user_repository import UserRepositoryBase
from app.application.interfaces.bid_repository import BidRepositoryBase
from app.application.dtos.bid import BidCreateDTO, BidResponseDTO
from app.application.mappers.bid_mapper import BidMapper
from app.application.interfaces.event_manager import EventManagerBase
from pydantic import EmailStr


class BidService():
    """
    Maneja la lógica de negocio relacionada con las ofertas (bids) y las interacciones entre usuarios y operaciones.
    """
    def __init__(self, bid_repository: BidRepositoryBase, user_repository: UserRepositoryBase, operation_repository: OperationRepositoryBase,
                 event_manager: EventManagerBase):
        """
        Inicializacion del servicio de ofertas con los repositorios de oferta, usuario y operación.

        Args:
            bid_repository (BidRepositoryBase): Repositorio de ofertas.
            user_repository (UserRepositoryBase): Repositorio de usuarios.
            operation_repository (OperationRepositoryBase): Repositorio de operaciones.
            event_manager (EventManager): Instancia del manejador de eventos
        """
        self.bid_repository = bid_repository
        self.user_repository = user_repository
        self.operation_repository = operation_repository
        self.event_manager = event_manager
    
    
    def create_bid(self, bid_dto: BidCreateDTO, bid_builder: BidBuilderBase):
        """
        Crea una nueva oferta si se cumplen todas las reglas de negocio.

        Args:
            bid_dto (BidCreateDTO): DTO con los datos de la oferta.
            bid_builder (BidBuilderBase): Builder para construir una nueva oferta.

        Raises:
            ValueError: Si el usuario no existe, no es tipo 'Investor', la operación no está disponible,
                        o el monto/tasa de interés no es válido.

        Returns:
            BidResponseDTO: La nueva oferta creada en formato DTO.
        """

        user_exists = self.user_repository.get_user_by_id(bid_dto.user_id)
        if user_exists is False:
            raise ValueError("El usuario no ha sido econtrado en la base de datos, verifique el user_id e intente nuevamente")
        elif user_exists.type != "Investor":
            raise ValueError("El usuario actual no tiene permitido crear este tipo de operaciones ya que no es de tipo Investor")
        
        operation = self.operation_repository.get(query={"id": bid_dto.operation_id})
        if operation is None:
            raise ValueError("La operación no existe.")
        if operation.status != "open":
            raise ValueError("La operación por la que intentas ofertar ya no se encuentra disponible.")
        if bid_dto.amount > int(operation.available_amount):
            raise ValueError("El monto de la oferta excede el monto disponible en la operación.")
        if bid_dto.interest_rate > operation.interest_rate:
            raise ValueError("La tasa de interés de la oferta es mayor que la tasa de la operación.")

        
        bid_builder.set_user_id(user_exists.id)
        bid_builder.set_amount(bid_dto.amount)
        bid_builder.set_interest_rate(bid_dto.interest_rate)
        bid_builder.set_operation_id(bid_dto.operation_id)
        new_bid = bid_builder.build()
        
        #evento que actualizara el monto disponible de la operacion ofertada
        event_data = {"operation_id": new_bid.operation_id, "amount": new_bid.amount}
        self.event_manager.notify("bid_created", event_data)
        
        self.bid_repository.save(BidMapper.to_entity_db(new_bid))
        return BidMapper.to_dto(new_bid)


    def get_all_bids_by_user(self, email):
        """
        Obtiene todas las ofertas creadas por un usuario.

        Args:
            email (str): Correo electrónico del usuario.

        Raises:
            ValueError: Si el usuario no existe, no es tipo 'Investor', o no tiene ofertas registradas.

        Returns:
            List[BidResponseDTO]: Una lista de DTOs de ofertas creadas por el usuario.
        """
        
        user_exists = self.user_repository.get_user_by_email(email)
        if user_exists is False:
            raise ValueError("El usuario no ha sido econtrado en la base de datos, verifique el user_id e intente nuevamente")
        elif user_exists.type != "Investor":
            raise ValueError("El usuario actual no tiene permitido crear este tipo de operaciones ya que no es de tipo Investor")

        
        query = {"user_id": user_exists.id}
        bids = self.bid_repository.get(query)
        if bids is False:
            raise ValueError("Error en la base de datos, intente nuevamente en unos minutos")
        if isinstance(bids, list):
            list_of_bids_to_return = []
            for operation in bids:
                list_of_bids_to_return.append(BidMapper.to_dto(operation))
            return list_of_bids_to_return
        return BidMapper.to_dto(bids)
    
    
    def get_bids_by_operation_id(self, operation_id: str, email: EmailStr):
        """
        Obtiene todas las ofertas de una operación específica.

        Args:
            operation_id (str): ID de la operación.
            email (EmailStr): Correo electrónico del operador que realiza la consulta.

        Raises:
            ValueError: Si el usuario no existe o no es tipo 'Operator', o si la operación no existe.

        Returns:
            List[BidResponseDTO]: Una lista de DTOs de ofertas para la operación.
        """
        user_exists = self.user_repository.get_user_by_email(email)
        if user_exists is False:
            raise ValueError("El usuario no ha sido econtrado en la base de datos, verifique el user_id e intente nuevamente")
        elif user_exists.type != "Operator":
            raise ValueError("El usuario actual no tiene permitido crear este tipo de operaciones ya que no es de tipo Operator")
        
        operation = self.operation_repository.get(query={"id": operation_id})
        if operation is None or operation is False:
            raise ValueError("La operación no existe.")


        
        query = {"operation_id": operation.id}
        bids = self.bid_repository.get(query)
        if bids is False:
            raise ValueError("Error en la base de datos, intente nuevamente en unos minutos")
        if isinstance(bids, list):
            list_of_bids_to_return = []
            for operation in bids:
                list_of_bids_to_return.append(BidMapper.to_dto(operation))
            return list_of_bids_to_return
        return BidMapper.to_dto(bids)