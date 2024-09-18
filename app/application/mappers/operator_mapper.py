from app.application.dtos.operation import OperationCreateDTO, OperationResponseDTO
from app.external.data_access.interfaces.operation import OperationDbBase
from app.core.entities.operation import OperationBase


class OperationMapper:
    
    
    @staticmethod
    def to_entity(operation_dto: OperationCreateDTO) -> OperationBase:
        return OperationBase(
            user_id=operation_dto.user_id,
            description=operation_dto.description,
            amount=operation_dto.amount,
            available_amount=int(operation_dto.amount),
            interest_rate=operation_dto.interest_rate,
            limit_date=operation_dto.limit_date,
        )
    
    @staticmethod
    def to_dto(operation_entity: OperationBase | OperationDbBase) -> OperationResponseDTO:
        return OperationResponseDTO(
            id=operation_entity.id,
            user_id=operation_entity.user_id,
            description=operation_entity.description,
            amount=operation_entity.amount,
            available_amount=int(operation_entity.available_amount),
            interest_rate=operation_entity.interest_rate,
            limit_date=operation_entity.limit_date,
            status=operation_entity.status,
            create_date=operation_entity.create_date,
            type=operation_entity.type
        )

    def to_entity_db(operation_entity: OperationBase) -> OperationDbBase:
        return OperationDbBase(
            id=operation_entity.id,
            user_id=operation_entity.user_id,
            description=operation_entity.description,
            amount=operation_entity.amount,
            available_amount=str(operation_entity.amount),
            interest_rate=operation_entity.interest_rate,
            limit_date=operation_entity.limit_date,
            status=operation_entity.status,
            create_date=operation_entity.create_date,
            type=operation_entity.type
        )
