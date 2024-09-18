from abc import ABC, abstractmethod

class BidBase(ABC):
    """
    Clase base abstracta para representar una oferta.

    Esta clase define los atributos básicos que toda oferta debe tener. 

    **Atributos:**
        * id (str): Identificador único de la oferta.
        * user_id (str): Identificador del usuario que realizó la oferta.
        * operation_id (str): Identificador de la operación a la que pertenece la oferta.
        * amount (float): Monto de la oferta.
        * interest_rate (float): Tasa de interés asociada a la oferta.
        * create_date (datetime): Fecha y hora en que se creó la oferta.
        * status (str): Estado actual de la oferta ("open", "closed", "reject").
        * type (str): Tipo de oferta (por ejemplo, "compra", "venta").
    """
    
    @property
    @abstractmethod
    def id(self):
        pass
    
    
    @property
    @abstractmethod
    def user_id(self):
        pass
    
    @property
    @abstractmethod
    def operation_id(self):
        pass
    
    
    @property
    @abstractmethod
    def amount(self):
        pass
    
    @property
    @abstractmethod
    def interest_rate(self):
        pass
    
    @property
    @abstractmethod
    def create_date(self):
        pass
    
    @property
    @abstractmethod
    def status(self):
        pass
    
    @property
    @abstractmethod
    def type(self):
        pass


class BidBuilderBase(ABC):
    """
    Clase base para construir objetos de tipo BidBase.
    """

    @abstractmethod
    def set_operation_id(self, operation_id):
        """
        Establece el identificador de la operación asociada a la oferta.

        Args:
            operation_id: Identificador de la operación.
        """
        pass

    @abstractmethod
    def set_user_id(self, user_id):
        """
        Establece el identificador del usuario que realiza la oferta.

        Args:
            user_id: Identificador del usuario.
        """
        pass

    @abstractmethod
    def set_amount(self, amount):
        """
        Establece el monto de la oferta.

        Args:
            amount: Monto de la oferta.
        """
        pass

    @abstractmethod
    def set_interest_rate(self, interest_rate):
        """
        Establece la tasa de interés de la oferta.

        Args:
            interest_rate: Tasa de interés de la oferta.
        """
        pass

    @abstractmethod
    def build(self) -> BidBase:
        """
        Construye y devuelve un objeto de tipo BidBase.

        Returns:
            BidBase: Objeto de tipo BidBase.
        """
        pass
