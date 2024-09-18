from abc import ABC, abstractmethod
from typing import Any

class UserRepositoryBase(ABC):
    """
    Clase base abstracta para el repositorio de usuarios.

    Esta clase define la interfaz para las operaciones básicas de persistencia
    y recuperación de usuarios. Todas las implementaciones concretas de
    repositorios de usuarios deben heredar de esta clase y proporcionar
    implementaciones para todos los métodos abstractos.
    """

    @abstractmethod
    def save(self, user: Any) -> None:
        """
        Guarda un usuario en el repositorio.

        Args:
            user (Any): El objeto usuario a guardar.

        Raises:
            NotImplementedError: Si el método no está implementado en la clase hija.
        """
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Any:
        """
        Recupera un usuario del repositorio por su dirección de correo electrónico.

        Args:
            email (str): La dirección de correo electrónico del usuario a buscar.

        Returns:
            Any: El objeto usuario correspondiente al correo electrónico proporcionado.

        Raises:
            NotImplementedError: Si el método no está implementado en la clase hija.
        """
        pass

    @abstractmethod
    def get_user_by_id(self, id: Any) -> Any:
        """
        Recupera un usuario del repositorio por su identificador único.

        Args:
            id (Any): El identificador único del usuario a buscar.

        Returns:
            Any: El objeto usuario correspondiente al identificador proporcionado.

        Raises:
            NotImplementedError: Si el método no está implementado en la clase hija.
        """
        pass

