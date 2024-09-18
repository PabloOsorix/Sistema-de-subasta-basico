from abc import ABC, abstractmethod


class OperationRepositoryBase(ABC):
    """
    Define los métodos base para las operaciones CRUD de OperationBase.
    """
    
    @abstractmethod
    def save(self, operation):
        """
        Guarda una operacion en el repositorio.

        Args:
            operacion (OperationBase): La operacion que se va a guardar.
        """
        pass
    
    @abstractmethod
    def get(self, query):
        """
        Obtiene una operacion o lista de operacions que cumplan con el query.

        Args:
            query (dict): Parámetros de búsqueda para obtener la operacion.
        """
        pass
    
    def delete(self, user_id: str, operation_id: str):
        """
        Elimina una operacion en función de su ID.

        Args:
            user_id: Identificador unico del usuario
            operacion_id (str): El identificador único de la operacion.
        """
        pass
    
    def update(self, operation):
        """
        Actualiza una operacion existente en el repositorio.

        Args:
            operacion (Operacion): La operacion que se va a actualizar.
        """
        pass




