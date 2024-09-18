from abc import ABC, abstractmethod


class BidRepositoryBase(ABC):
    """
    Define los métodos base para las operaciones CRUD de las ofertas (bids).
    """

    @abstractmethod
    def save(self, bid):
        """
        Guarda una oferta en el repositorio.

        Args:
            bid (Bid): La oferta que se va a guardar.
        """
        pass

    @abstractmethod
    def get(self, query):
        """
        Obtiene una oferta o lista de ofertas que cumplan con el query.

        Args:
            query (dict): Parámetros de búsqueda para obtener la oferta.
        """
        pass

    def delete(self, bid_id: str):
        """
        Elimina una oferta en función de su ID.

        Args:
            bid_id (str): El identificador único de la oferta.
        """
        pass

    def update(self, bid):
        """
        Actualiza una oferta existente en el repositorio.

        Args:
            bid (Bid): La oferta que se va a actualizar.
        """
        pass

