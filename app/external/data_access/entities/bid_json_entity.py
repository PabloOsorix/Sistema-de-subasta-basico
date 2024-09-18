from app.external.data_access.interfaces.bid import BidDbBase


class BidJsonEntity(BidDbBase):
    def __init__(self, id, user_id, operation_id, amount, interest_rate, create_date, status, type) -> None:
        super().__init__(id, user_id, operation_id, amount, interest_rate, create_date, status, type)

