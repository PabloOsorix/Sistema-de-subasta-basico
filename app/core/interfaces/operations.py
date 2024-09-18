from abc import ABC, abstractmethod


class OperationBase(ABC):
    """
    Clase base abstracta que define la estructura común para todas las operaciones.

    Esta clase proporciona los atributos básicos que toda operación debe tener.

    **ATRIBUTOS**
        id (str): Identificador único de la operación.
        user_id (str): Identificador del usuario asociado a la operación.
        description (str): Descripción detallada de la operación.
        amount (float): Monto total de la operación.
        available_amount (float): Monto disponible dentro de la operación.
            Este atributo debe ser implementado por las clases hijas.
        interest_rate (float): Tasa de interés aplicada a la operación.
        limit_date (datetime): Fecha límite para la operación.
        status (str): Estado actual de la operación (por ejemplo, "pendiente", "completado", "cancelado").
            Este atributo debe ser implementado por las clases hijas.
        create_date (datetime): Fecha y hora de creación de la operación.
        type (str): Tipo de operación (por ejemplo, "pago", "transferencia", "inversión").
            Este atributo debe ser implementado por las clases hijas.

    Métodos:
        Los métodos de esta clase son propiedades abstractas y deben ser implementados
        por las clases hijas para proporcionar la lógica específica de cada tipo de operación.
    """
    @property
    @abstractmethod
    def id():
        pass
    
    @property
    @abstractmethod
    def user_id():
        pass
    
    @property
    @abstractmethod
    def description():
        pass
    
    @property
    @abstractmethod
    def amount():
        pass
    
    @property
    def available_amount(self):
        pass

    @property
    @abstractmethod
    def interest_rate():
        pass

    @property
    @abstractmethod
    def limit_date():
        pass
    
    @property
    @abstractmethod
    def status():
        pass
    
    @property
    @abstractmethod
    def create_date():
        pass
    
    @property
    @abstractmethod
    def type():
        pass
    
    
class OperationBaseFactory(ABC):
    """
    Fábrica base para la creación de operaciones.

    Esta clase define un método abstracto para crear nuevas operaciones.

    **Métodos:**
        new_operation(self, user_id, description, amount, available_amount, interest_rate, limit_date):
            Crea una nueva operación.

            **Args:**
                * user_id (str): Identificador del usuario que crea la operación.
                * description (str): Descripción de la operación.
                * amount (float): Monto total de la operación.
                * available_amount (float): Monto disponible para la operación.
                * interest_rate (float): Tasa de interés aplicada a la operación.
                * limit_date (datetime): Fecha límite para la operación.

            **Returns:**
                OperationBase: Una instancia de una clase hija de OperationBase que representa la operación creada.
    """
    @abstractmethod
    def new_operation(self, user_id, description, amount, available_amount, interest_rate, limit_date):
        pass