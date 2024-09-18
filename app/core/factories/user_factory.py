from app.core.interfaces.user import UserBase, UserFactoryBase
from app.core.entities.user import Operator, Investor

# decidi crear multiples fabricas para respetar el principio SRP
class OperatorUserFactory(UserFactoryBase):
    """"""
    def __init__(self) -> None:
        pass
    
    @classmethod
    def create_new_user(self, username, email, password):
        return Operator(username, email, password)


class InvestorUserFactory(UserFactoryBase):
    def __init__(self) -> None:
        pass
    
    @classmethod
    def create_new_user(self, username, email, password):
        return Investor(username, email, password)


class UserFactory(UserFactoryBase):
    """
    Una fábrica para crear diferentes tipos de usuarios.

    Esta clase hereda de UserFactoryBase y proporciona un método
    para crear instancias de diferentes tipos de usuarios.

    Attributes:
        _user_types (dict): Un diccionario que mapea los tipos de usuario
            a sus respectivas clases.
    """
    
    _user_types = {
        'operator': Operator,
        'investor': Investor
    }


    @classmethod
    def create_new_user(cls, username: str, email: str, password: str, type: str) -> UserBase:
        """
        Crea y retorna una nueva instancia de usuario del tipo especificado.

        Args:
            username (str): El nombre de usuario para el nuevo usuario.
            email (str): La dirección de correo electrónico del nuevo usuario.
            password (str): La contraseña del nuevo usuario.
            type (str): El tipo de usuario a crear ('operator' o 'investor').

        Returns:
            UserBase: Una instancia de una subclase apropiada de UserBase.

        Raises:
            ValueError: Si el tipo de usuario especificado no es reconocido.
        """
        user_class = cls._user_types.get(type.lower())
        if not user_class:
            raise ValueError(f"Tipo de usuario '{type}' no reconocido.")
        return user_class(username, email, password)