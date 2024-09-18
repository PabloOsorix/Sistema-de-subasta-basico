from app.application.interfaces.bid_repository import BidRepositoryBase
from app.external.data_access.entities.bid_json_entity import BidJsonEntity
import os
import json
from app.databases import json_bids_database_path


class JsonBidRepository(BidRepositoryBase):
    """
      Repositorio para manejar las ofertas (bids) almacenadas en un archivo JSON.
    """
    def __init__(self):
        """
        Inicializa el repositorio de ofertas con la ruta del archivo JSON.
        """
        self.file_path = json_bids_database_path

    def save(self, bid: BidJsonEntity):
        """
        Guarda una nueva oferta en el archivo JSON.

        Args:
            bid (BidJsonEntity): La oferta que se va a guardar.

        Returns:
            bool: Retorna True si la oferta se guarda correctamente, False en caso de error.
        """
        bids = self.read()
        bids.append(bid.__dict__)
        result = self.write(bids)
        if result is False:
            return False
        return True

    # Aqui podriamos implementar un patron composite, (es demasiado
    # extenso para la prueba.)
    def get(self, query: dict) -> BidJsonEntity | list[BidJsonEntity] | bool:
        """
        Method: get
        Obtiene una oferta o una lista de ofertas que coincidan con el query especificado.

        Args:
            query (dict): Parámetros para buscar las ofertas.

        Returns:
            BidJsonEntity | list[BidJsonEntity] | bool: Retorna una oferta, una lista de ofertas o False si no encuentra coincidencias.
        """
        bids = self.read()
        list_bids = []

        for bid in bids:
            if all(bid.get(filter_key) == filter_value for filter_key, filter_value in query.items()):
                list_bids.append(BidJsonEntity(**bid))

        if len(list_bids) >= 2:
            return list_bids
        elif len(list_bids) == 1:
            return list_bids[0]
        return False

    def update(self, bid_to_update=BidJsonEntity):
        """
        Method: update
        Actualiza una oferta existente en el archivo JSON.

        Args:
            bid_to_update (BidJsonEntity): La oferta con los datos actualizados.

        Returns:
            bool: Retorna True si la actualización fue exitosa, False en caso de error.
        """
        bid_to_update = bid_to_update.__dict__
        _not_editables = ["id", "user_id", "create_date", "type", "operation_id"]
        operations = self.read()
        
        for count, operation in enumerate(operations):
            if operation.get("id") == bid_to_update.get("id"):
                for property in operation:
                    if property not in _not_editables\
                    and bid_to_update.get(property) != operation.get(property)\
                    and bid_to_update.get(property) and bid_to_update.get(property) != None:
                        operations[count][property] = bid_to_update[property]


        result = self.write(operations)
        if result is False:
            return False
        return True

    def delete(self, user_id: str, bid_id: str):
        """
        Marca una oferta como eliminada (cambia el status a 'delete') en el archivo JSON.

        Args:
            user_id (str): El ID del usuario dueño de la oferta.
            bid_id (str): El ID de la oferta a eliminar.

        Returns:
            bool: Retorna True si la eliminación fue exitosa, False en caso de error.
        """
        bids = self.read()
        for count, bid in enumerate(bids):
            if bid.get("user_id") == user_id and bid.get("id") == bid_id:
                bids[count]["status"] = "delete"
                break
        result = self.write(bids)
        if result is False:
            return False
        return True

    def read(self) -> list:
        """
        Lee y retorna todas las ofertas almacenadas en el archivo JSON.

        Returns:
            list: Lista de ofertas almacenadas en el archivo JSON.
        """
        with open(self.file_path, '+r', encoding="utf-8") as file:
            data = json.load(file)
            if len(data) < 1:
                data["bids"] = []
            return data["bids"]

    def write(self, data: list) -> bool:
        """
        Escribe los datos en el archivo JSON.

        Args:
            data (list): Lista de ofertas a escribir en el archivo.

        Returns:
            bool: Retorna True si la escritura fue exitosa, False en caso de error.
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({"bids": data}, file, ensure_ascii=False, indent=4)
            return True
        return False
