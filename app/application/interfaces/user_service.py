from app.application.interfaces.user_repository import UserRepositoryBase
from app.application.dtos.user import UserCreateDTO, UserResponseDTO
from app.application.mappers.user_mapper import UserMapper
from app.core.interfaces.user import UserFactoryBase
from app.utils.hasher import hash_sensible_data, check_hashed_data

class UserService():
    """
    Servicio para la gestión de usuarios.

    Esta clase proporciona métodos para crear nuevos usuarios y recuperar
    información de usuarios existentes.

    Attributes:
        user_repository (UserRepositoryBase): Repositorio para el almacenamiento y recuperación de usuarios.
    """
    def __init__(self, user_repository: UserRepositoryBase) -> None:
        """
        Inicializa el servicio de usuarios con el repositorio especificado.

        Args:
            user_repository (UserRepositoryBase): Repositorio de usuarios.
        """
        self.user_repository = user_repository

        
    
    def create_new_user(self, user_dto: UserCreateDTO, user_factory: UserFactoryBase):
        """
        Crea un nuevo usuario en el sistema.

        Este método realiza las siguientes operaciones:
        1. Verifica si el usuario ya existe en la base de datos.
        2. Hashea la contraseña del usuario.
        3. Crea un nuevo usuario utilizando la fábrica proporcionada.
        4. Guarda el nuevo usuario en el repositorio.
        5. Retorna un DTO del usuario creado.

        Args:
            user_dto (UserCreateDTO): DTO con la información del nuevo usuario.
            user_factory (UserFactoryBase): Fábrica para crear nuevos usuarios.

        Returns:
            Any: DTO del usuario creado.

        Raises:
            ValueError: Si el usuario ya existe en el sistema.
        """
        user_exists = self.user_repository.get_user_by_email(user_dto.email)
        if user_exists is not False:
            raise ValueError("El usuario ya tiene una cuenta existente")

        
        hashed_password = hash_sensible_data(user_dto.password)
        
        new_user = user_factory.create_new_user(username=user_dto.username.lower(), email=user_dto.email, password=hashed_password, type=user_dto.type)
        self.user_repository.save(UserMapper.to_entity_db(new_user))
        return UserMapper.to_dto(new_user)


    def get_user_by_email(self, email, password=False):
        """
        Recupera un usuario por su dirección de correo electrónico.

        Args:
            email (str): Dirección de correo electrónico del usuario.
            password (bool, optional): Indica si se debe incluir la contraseña en la respuesta. 
                                       Por defecto es False.

        Returns:
            Any: Si password es True, devuelve el objeto usuario completo.
                 Si password es False, devuelve un DTO del usuario.

        Raises:
            ValueError: Si el usuario no se encuentra en el sistema.
        """
        user = self.user_repository.get_user_by_email(email)
        if user is False:
            raise ValueError("El usuario no fue encontrado, revise que los datos sean correctos")
        if password is True:
            return user
        user_dto = UserMapper.to_dto(user)
        return user_dto
