from app.application.interfaces.operation_repository import OperationRepositoryBase
from app.core.entities.operation import OperationBaseFactory
from app.core.validators.validators import AmountValidator, LimitDateValidator, InterestRateValidator
from app.application.interfaces.user_repository import UserRepositoryBase
from app.application.dtos.operation import OperationCreateDTO
from app.application.mappers.operator_mapper import OperationMapper
from pydantic import EmailStr

class OperationService():
    """
    Maneja la lógica de negocio relacionada con las operaciones (Operation) y las interacciones entre usuarios.
    """

    def __init__(self, operation_repository: OperationRepositoryBase, user_repository: UserRepositoryBase) -> None:
        """
        Inicializacion del servicio de operaciones con los repositorios de operaciones y usuario.

        Args:
            operation_repository (OperationRepositoryBase): Repositorio de operaciones.
            user_repository (UserRepositoryBase): Repositorio de usuarios.
        """
        self.operation_repository = operation_repository
        self.user_repository = user_repository

    def create_operation(self, operation_dto: OperationCreateDTO, operation_factory: OperationBaseFactory):
        """
        Crea una nueva oepracion si se cumplen todas las reglas de negocio.

        Args:
            oepration_dto (OperationCreateDTO): DTO con los datos de la operacion a crear.
            operation_factory (OperationBaseFactory): Facotory para construir una nueva operacion.

        Raises:
            ValueError: Si el usuario no existe o  no es tipo 'Operator'.

        Returns:
            OperationResponseDTO: La nueva operacion creada en formato DTO.
        """

        user_exists = self.user_repository.get_user_by_id(operation_dto.user_id)
        if user_exists is False:
            raise ValueError("El usuario no ha sido econtrado en la base de datos, verifique el user_id e intente nuevamente")
        elif user_exists.type != "Operator":
            raise ValueError("El usuario actual no tiene permitido crear este tipo de operaciones ya que no es de tipo Operador")
        

        AmountValidator.validate(operation_dto.amount)
        InterestRateValidator.validate(operation_dto.interest_rate)
        LimitDateValidator.validate(operation_dto.limit_date)

        new_operation = operation_factory.new_operation(
            user_id=user_exists.id,
            description=operation_dto.description,
            amount=operation_dto.amount,
            available_amount=operation_dto.amount,
            interest_rate=operation_dto.interest_rate,
            limit_date=operation_dto.limit_date
        )
        self.operation_repository.save(OperationMapper.to_entity_db(new_operation))
        return OperationMapper.to_dto(new_operation)

    def get_all_operations_by_user_id(self, user_id):
        """
        Obtiene todas las operaciones creadas por un usuario.

        Args:
            user_id (str): Identificador único del usuario en el sistema. 
                        Este valor debe ser de tipo string

        Returns:
            List[dict]: Una lista de diccionarios. Cada diccionario representa una operación 
                    y contiene los siguientes campos (ajusta según tu modelo de datos):
                    - id (str): Identificador único de la operación.
                    - user_id (str): Identificador del usuario al que pertenece la operación.
                    - amount (int): Monto total de la operación.
                    - available_amount (int): Monto disponible para la operación.
                    - interest_rate (float): Tasa de interés maxima que el operador esta dispuesto a pagar.
                    - limit_date (str): Fecha límite para la operación.
                    - state (str): Estado actual de la operación (por ejemplo, 'open', 'close').
                    - create_date (str): Fecha de creación de la operación.
                    - type (str): Tipo de operación (por ejemplo, 'StandardOperation', 'TransferentialOperation').

        Raises:
            ValueError: Si el `user_id` proporcionado no es operador o no existe.
            ValueError: Si el usuario no tiene ninguna operacion registrada
        """
        user_exists = self.user_repository.get_user_by_id(user_id)
        if user_exists is False:
            raise ValueError("El usuario no ha sido econtrado en la base de datos, verifique el user_id e intente nuevamente")
        elif user_exists.type != "Operator":
            raise ValueError("El usuario actual no tiene permitido crear este tipo de operaciones ya que no es de tipo Operador")
        
        query = {"user_id": user_exists.id}
        operations = self.operation_repository.get(query)
        if operations is False:
            raise ValueError("El usuario actual no ha creado operaciones")
        if isinstance(operations, list):
            list_of_operations_to_return = []
            for operation in operations:
                list_of_operations_to_return.append(OperationMapper.to_dto(operation))
            return list_of_operations_to_return
        return OperationMapper.to_dto(operations)
        
    def get_all_open(self):
        """
        Obtiene todas las operaciones activas creadas por un usuario.

        Args:
            user_id (str): Identificador único del usuario en el sistema. 
                        Este valor debe ser de tipo string

        Returns:
            List[dict]: Una lista de diccionarios. Cada diccionario representa una operación 
                    y contiene los siguientes campos (ajusta según tu modelo de datos):
                    - id (str): Identificador único de la operación.
                    - user_id (str): Identificador del usuario al que pertenece la operación.
                    - amount (int): Monto total de la operación.
                    - available_amount (int): Monto disponible para la operación.
                    - interest_rate (float): Tasa de interés maxima que el operador esta dispuesto a pagar.
                    - limit_date (str): Fecha límite para la operación.
                    - state (str): Estado actual de la operación (por ejemplo, 'open', 'close').
                    - create_date (str): Fecha de creación de la operación.
                    - type (str): Tipo de operación (por ejemplo, 'StandardOperation', 'TransferentialOperation').

        Raises:
            ValueError: Si el `user_id` proporcionado no es operador o no existe.
            ValueError: Si el usuario no tiene ninguna operacion registrada
        """
        
        query = {"status": "open"}
        operations = self.operation_repository.get(query)
        if operations is False:
            raise ValueError("Error en la base de datos, intente nuevamente en unos minutos")
        if isinstance(operations, list):
            list_of_operations_to_return = []
            for operation in operations:
                list_of_operations_to_return.append(OperationMapper.to_dto(operation))
            return list_of_operations_to_return
        return OperationMapper.to_dto(operations)


    def get_operation_by_id(self, operation_id:str):
        """
        Obtiene una operacion por el id de esta

        Args:
            operation_id (str): Identificador único de la operacion en el sistema. 
                        Este valor debe ser de tipo string

        Returns:
            List[dict]: Una lista de diccionarios. Cada diccionario representa una operación 
                    y contiene los siguientes campos (ajusta según tu modelo de datos):
                    - id (str): Identificador único de la operación.
                    - user_id (str): Identificador del usuario al que pertenece la operación.
                    - amount (int): Monto total de la operación.
                    - available_amount (int): Monto disponible para la operación.
                    - interest_rate (float): Tasa de interés maxima que el operador esta dispuesto a pagar.
                    - limit_date (str): Fecha límite para la operación.
                    - state (str): Estado actual de la operación (por ejemplo, 'open', 'close').
                    - create_date (str): Fecha de creación de la operación.
                    - type (str): Tipo de operación (por ejemplo, 'StandardOperation', 'TransferentialOperation').

        Raises:
            ValueError: Si el `user_id` proporcionado no es operador o no existe.
            ValueError: Si el usuario no tiene ninguna operacion registrada
        """
        
        query = {"status": "open", "id": operation_id}
        operation = self.operation_repository.get(query)
        if operation is False:
            raise ValueError("Error en la base de datos, intente nuevamente en unos minutos")
        return OperationMapper.to_dto(operation)
    
    def delete(self, user_id: str, operation_id: str, email: EmailStr):
        """
        Elimina una operacion por su id.

        Args:
            email (str): Correo electrónico del usuario.
            user_id (str): identificador del usuario.
            operation_id (str): identificador de la operacion que se eliminara.

        Raises:
            ValueError: Si el usuario no existe, no es de tipo operador, la operacion no existe,
            la operacion no pertenece al usuario o la operacion ya ha sido eliminada

        Returns:
            True si el usuario ha sido eliminado
        """
        
        user_origin = self.user_repository.get_user_by_email(email)
        print(user_origin)
        user_exists = self.user_repository.get_user_by_id(user_id)
        if user_exists is False:
            raise ValueError("El usuario no ha sido econtrado en la base de datos, verifique el user_id e intente nuevamente")
        elif user_exists is False:
            raise ValueError("El usuario no ha sido econtrado en la base de datos que realiza la peticion no ha sido encontrado en la base de datos")
        elif user_exists.type != "Operator":
            raise ValueError("El usuario actual no tiene permitido borrar operaciones ya que no es de tipo Operador")
        elif user_exists.id != user_origin.id:
              raise ValueError("El user_id enviado no coincide con el usuario que realiza la peticion")
        
        query = {"user_id": user_origin.id, "id": operation_id}
        operation_exists = self.operation_repository.get(query)
        
        if operation_exists is False:
            raise ValueError("La operacion no fue encontrada en base de datos, verifique el operation_id e intente nuevamente")
        elif operation_exists.state == "delete":
            raise ValueError("La operacion ya ha sido eliminada")
            
        
        operation_deleted = self.operation_repository.delete(user_id, operation_exists.id)
        
        if operation_deleted is False:
            raise ValueError("Hubo un error intentando eliminar la operacion, intente nuevamente en unos minutos")
        return True