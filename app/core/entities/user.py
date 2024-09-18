from abc import abstractmethod
from app.core.interfaces.user import UserBase
from datetime import datetime
from uuid import uuid4



class Operator(UserBase):
    """
    Representa un usuario de tipo Operador en el sistema.

    Esta clase hereda de UserBase y proporciona una implementación
    específica para los usuarios de tipo Operador.

    Attributes:
        _id (str): Identificador único del operador.
        _username (str): Nombre de usuario del operador.
        _email (str): Dirección de correo electrónico del operador.
        _password (str): Contraseña del operador.
        _create_date (str): Fecha y hora de creación del operador.
        _type (str): Tipo de usuario, en este caso 'Operator'.
    """

    def __init__(self, username: str, email: str, password: str) -> None:
        """
        Inicializa una nueva instancia de Operator.

        Args:
            username (str): El nombre de usuario del operador.
            email (str): La dirección de correo electrónico del operador.
            password (str): La contraseña del operador.
        """
        self._id = str(uuid4())
        self._username = username
        self._email = email
        self._password = password
        self._create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._type = self.__class__.__name__.__str__()
        
    @property
    def id(self) -> str:
        """str: El identificador único del operador."""
        return self._id
    
    @property
    def username(self) -> str:
        """str: El nombre de usuario del operador."""
        return self._username
        
    @property
    def email(self) -> str:
        """str: La dirección de correo electrónico del operador."""
        return self._email
    
    @property
    def password(self) -> str:
        """str: La contraseña del operador."""
        return self._password
    
    @property
    def create_date(self) -> str:
        """str: La fecha y hora de creación del operador."""
        return self._create_date
    
    @property
    def type(self) -> str:
        """str: El tipo de usuario, en este caso 'Operator'."""
        return self._type


class Investor(UserBase):
   """
   Representa un usuario de tipo Inversor en el sistema.

   Esta clase hereda de UserBase y proporciona una implementación
   específica para los usuarios de tipo Inversor.

   Attributes:
       _id (str): Identificador único del inversor.
       _username (str): Nombre de usuario del inversor.
       _email (str): Dirección de correo electrónico del inversor.
       _password (str): Contraseña del inversor.
       _create_date (str): Fecha y hora de creación del inversor.
       _type (str): Tipo de usuario, en este caso 'Investor'.
   """

   def __init__(self, username: str, email: str, password: str) -> None:
       """
       Inicializa una nueva instancia de Investor.

       Args:
           username (str): El nombre de usuario del inversor.
           email (str): La dirección de correo electrónico del inversor.
           password (str): La contraseña del inversor.
       """
       self._id = str(uuid4())
       self._username = username
       self._email = email
       self._password = password
       self._create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       self._type = self.__class__.__name__.__str__()
       
   @property
   def id(self) -> str:
       """str: El identificador único del inversor."""
       return self._id
   
   @property
   def username(self) -> str:
       """str: El nombre de usuario del inversor."""
       return self._username
       
   @property
   def email(self) -> str:
       """str: La dirección de correo electrónico del inversor."""
       return self._email
   
   @property
   def password(self) -> str:
       """str: La contraseña del inversor."""
       return self._password
   
   @property
   def create_date(self) -> str:
       """str: La fecha y hora de creación del inversor."""
       return self._create_date
   
   @property
   def type(self) -> str:
       """str: El tipo de usuario, en este caso 'Investor'."""
       return self._type