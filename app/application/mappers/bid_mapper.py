from app.application.dtos.bid import BidCreateDTO, BidResponseDTO
from app.external.data_access.interfaces.bid import BidDbBase
from app.core.entities.bid import BidBase


class BidMapper:
    
    
    @staticmethod
    def to_entity(operation_dto:  BidCreateDTO) -> BidBase:
        return BidBase(
            user_id=operation_dto.user_id,
            amount=operation_dto.amount,
            available_amount=operation_dto.amount,
            interest_rate=operation_dto.interest_rate,
            limit_date=operation_dto.limit_date,
        )

    @staticmethod
    def to_dto(bid_entity: BidBase | BidDbBase) -> BidResponseDTO:
        return BidResponseDTO(
            id=bid_entity.id,
            operation_id=bid_entity.operation_id,
            amount=bid_entity.amount,
            interest_rate=bid_entity.interest_rate,
            create_date=bid_entity.create_date,
            status=bid_entity.status,
        )

    def to_entity_db(bid_entity: BidBase) -> BidResponseDTO:
        return BidDbBase(
            id=bid_entity.id,
            user_id=bid_entity.user_id,
            operation_id=bid_entity.operation_id,
            amount=bid_entity.amount,
            interest_rate=bid_entity.interest_rate,
            create_date=bid_entity.create_date,
            status=bid_entity.status,
            type=bid_entity.type
        )
        