from app.application.dtos.user import UserCreateDTO, UserResponseDTO
from app.external.data_access.interfaces.user import UserDbBase
from app.core.entities.user import UserBase


class UserMapper:
    
    
    @staticmethod
    def to_entity(user_dto: UserCreateDTO) -> UserBase:
        return UserBase(
            id=user_dto.id,
            username=user_dto.username,
            email=user_dto.email,
            hashed_password=user_dto.password,
            type=user_dto.type,
            create_date=user_dto.create_date
        )
    
    @staticmethod
    def to_dto(user_entity: UserBase | UserDbBase) -> UserResponseDTO:
        return UserResponseDTO(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            type=user_entity.type
        )

    def to_entity_db(user_entity: UserBase) -> UserDbBase:
        return UserDbBase(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            hashed_password=user_entity.password,
            type=user_entity.type,
            create_date=user_entity.create_date
        )
        
        
