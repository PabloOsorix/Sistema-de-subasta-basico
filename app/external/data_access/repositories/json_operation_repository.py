from app.application.interfaces.operation_repository import OperationRepositoryBase
import os
import json
from app.external.data_access.entities.operation_json_entity import OperationJsonEntity
from app.databases import json_operations_database_path


class JsonOperationRepository(OperationRepositoryBase):
    """
    Repositorio para manejar las operaciones almacenadas en un archivo JSON.
    """
    def __init__(self):
        """
        Inicializa el repositorio de operaciones con la ruta del archivo JSON.
        """
        self.file_path = json_operations_database_path

    def save(self, operation: OperationJsonEntity):
        """
        Guarda una nueva operación en el archivo JSON.

        Args:
            operation (OperationJsonEntity): La operación que se va a guardar.

        Returns:
            bool: Retorna True si la operación se guarda correctamente, False en caso de error.
        """
        operations = self.read()
        operations.append(operation.__dict__)
        result = self.write(operations)
        if result is False:
            return False
        return True

    # Aqui podriamos implementar un patron composite, (es demasiado
    # extenso para la prueba.)
    def get(self, query: dict) -> OperationJsonEntity | list[OperationJsonEntity] | bool:
        """
        Obtiene una operación o una lista de operaciones que coincidan con el query especificado.

        Args:
            query (dict): Parámetros para buscar las operaciones.

        Returns:
            OperationJsonEntity | list[OperationJsonEntity] | bool: Retorna una operación, una lista de operaciones o False si no encuentra coincidencias.
        """
        operations = self.read()
        list_operations = []

        for operation in operations:
            if all(operation.get(filter_key) == filter_value for filter_key, filter_value in query.items()):
                list_operations.append(OperationJsonEntity(**operation))

        if len(list_operations) >= 2:
            return list_operations
        elif len(list_operations) == 1:
            return list_operations[0]
        return False

    def update(self, operation_up: OperationJsonEntity):
        """
        Actualiza una operación existente en el archivo JSON.

        Args:
            operation_up (OperationJsonEntity): La operación con los datos actualizados.

        Returns:
            bool: Retorna True si la actualización fue exitosa, False en caso de error.
        """
        operation_up = operation_up.__dict__
        _not_editables = ["id", "user_id", "create_date", "type"]
        operations = self.read()
        
        for count, operation in enumerate(operations):
            if operation.get("id") == operation_up.get("id"):
                for property in operation:
                    if property not in _not_editables\
                    and operation_up.get(property) != operation.get(property)\
                    and operation_up.get(property) and operation_up.get(property) != None:
                        operations[count][property] = operation_up[property]


        result = self.write(operations)
        if result is False:
            return False
        return True
    
    def update_available_amount(self, operation_id: str, bid_amount: int):
        """
        Method: update_available_amount
        Actualiza el monto disponible de una operación restando el monto de la oferta.

        Args:
            operation_id (str): El ID de la operación.
            bid_amount (int): El monto de la oferta.

        Returns:
            bool: Retorna True si la actualización fue exitosa, False en caso de error.
        """
        operation = self.get({"id": operation_id})
        if operation is False:
            return False
        
        operation.available_amount = int(operation.available_amount) - bid_amount
        if operation.available_amount == 0:
            operation.available_amount = "0"
        
        result = self.update(operation)
        if result is False:
            return False
        return True

    def delete(self, user_id: str, operation_id: str):
        """
        Marca una operación como eliminada (cambia el status a 'delete') en el archivo JSON.

        Args:
            user_id (str): El ID del usuario dueño de la operación.
            operation_id (str): El ID de la operación a eliminar.

        Returns:
            bool: Retorna True si la eliminación fue exitosa, False en caso de error.
        """
        operations = self.read()
        for count, operation in enumerate(operations):
            if operation.get("user_id") == user_id and operation.get("id") == operation_id:
                operations[count]["status"] = "delete"
                break
        result = self.write(operations)
        if result is False:
            return False
        return True

    def read(self) -> list:
        """
        Lee y retorna todas las operaciones almacenadas en el archivo JSON.

        Returns:
            list: Lista de operaciones almacenadas en el archivo JSON.
        """
        with open(self.file_path, '+r', encoding="utf-8") as file:
            data = json.load(file)
            return data["operations"]

    def write(self, data: list) -> bool:
        """
        Escribe los datos en el archivo JSON.

        Args:
            data (list): Lista de operaciones a escribir en el archivo.

        Returns:
            bool: Retorna True si la escritura fue exitosa, False en caso de error.
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({"operations": data}, file, ensure_ascii=False, indent=4)
            return True
        return False
