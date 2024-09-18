# Dependencia para obtener la sesión de la base de datos en cada request
import os
import json
from app.application.interfaces.user_repository import UserRepositoryBase
from app.external.data_access.entities.user_json_entity import UserJsonEntity
from app.databases import json_users_database_path

class JsonUserRepository(UserRepositoryBase):
    """
    Repositorio para manejar los usuarios almacenados en un archivo JSON.
    """
    def __init__(self, file_path=json_users_database_path):
        """
        Inicializa el repositorio de usuarios con la ruta del archivo JSON.

        Args:
            file_path (str): Ruta del archivo JSON de usuarios.
        """
        self.file_path = file_path


    def get_user_by_email(self, email) -> UserJsonEntity:
        """
        Obtiene un usuario a partir de su correo electrónico.

        Args:
            email (str): Correo electrónico del usuario.

        Returns:
            UserJsonEntity | bool: Retorna el usuario si es encontrado, False en caso contrario.
        """
        users = self.read()["users"]
        for user in users:
            if user.get("email") == email:
                return UserJsonEntity(
                    id=user["id"],
                    username=user["username"],
                    email=user["email"],
                    hashed_password=str(user["hashed_password"]),
                    type=user["type"],
                    create_date=user["create_date"]
                )
        return False
    
    def get_user_by_id(self, id) -> UserJsonEntity:
        """
        Method: get_user_by_id
        Obtiene un usuario a partir de su ID.

        Args:
            id (str): El ID del usuario.

        Returns:
            UserJsonEntity | bool: Retorna el usuario si es encontrado, False en caso contrario.
        """
        users = self.read()["users"]
        for user in users:
            if user.get("id") == id:
                return UserJsonEntity(
                    id=user["id"],
                    username=user["username"],
                    email=user["email"],
                    hashed_password=str(user["hashed_password"]),
                    type=user["type"],
                    create_date=user["create_date"]
                )
        return False


    def save(self, user: UserJsonEntity) -> None:
        """
        Guarda un nuevo usuario en el archivo JSON.

        Args:
            user (UserJsonEntity): El usuario que se va a guardar.
        """
        updated_db = self.read()
        updated_db["users"].append(user.__dict__)
        with open(self.file_path, "+w", encoding='utf-8') as json_db:
            json.dump(updated_db, json_db,  ensure_ascii=True, indent=4, default=str)
    
    def read(self) -> list:
        """
        Lee y retorna todos los usuarios almacenados en el archivo JSON.

        Returns:
            list: Lista de usuarios almacenados en el archivo JSON.
        """
        with open(self.file_path, '+r', encoding="utf-8") as file:
            data = json.load(file)
            return data