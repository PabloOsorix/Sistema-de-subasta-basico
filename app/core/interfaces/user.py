from abc import ABC, abstractmethod


class UserBase(ABC):
    """
    Clase base para entidades de usuario.

    *(Atributos)*
    id (str): identificador único del usuario.
    username (str): nombre de usuario del usuario.
    create_date (datetime): fecha y hora en que se creó el usuario.
    email (str): dirección de correo electrónico del usuario.
    password (str): contraseña del usuario.
    type (str): tipo de usuario (p. ej., "admin", "customer"). Debe ser implementado por clases secundarias.
    """

    @property
    @abstractmethod
    def id(self):
        """
        Returns:
            str: identificador unico del usuario.
        """
        pass

    @property
    @abstractmethod
    def username(self):
        """
        Returns:
            str: Nombre de usuario.
        """
        pass

    @property
    @abstractmethod
    def create_date(self):
        """
        Returns:
            datetime: Fecha de creacion del usuario.
        """
        pass

    @property
    @abstractmethod
    def email(self):
        """
        Returns:
            str: correo electronico del usuario.
        """
        pass

    @property
    @abstractmethod
    def password(self):
        """
        Returns:
            str: Contrasena del usuario.
        """
        pass

    @property
    @abstractmethod
    def type(self):
        """
        Returns:
            str: Tipo de usuario ("Operator", "Investor").
        """
        pass



class UserFactoryBase(ABC):
   """
   Clase base abstracta para fábricas de usuarios.

   Esta clase define la interfaz para crear nuevos usuarios
   en el sistema. Las clases concretas que hereden de esta
   deben implementar el método create_new_user.
   """
   
   @abstractmethod
   def create_new_user(self, username: str, email: str, password: str, type: str):
       """
       Método abstracto para crear un nuevo usuario.

       Este método debe ser implementado por las clases hijas para
       proporcionar la lógica específica de creación de usuarios.

       Args:
           username (str): El nombre de usuario para el nuevo usuario.
           email (str): La dirección de correo electrónico del nuevo usuario.
           password (str): La contraseña del nuevo usuario.
           type (str): El tipo de usuario a crear.

       Returns:
           Un objeto de usuario del tipo especificado.

       Raises:
           NotImplementedError: Si este método no es implementado por la clase hija.
       """
       pass