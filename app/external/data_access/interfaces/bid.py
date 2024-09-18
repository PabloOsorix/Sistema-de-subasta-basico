from abc import ABC

class BidDbBase(ABC):
    def __init__(self, id, user_id, operation_id, amount, interest_rate, create_date, status, type) -> None:
        self.id = id
        self.user_id = user_id
        self.operation_id = operation_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.create_date = create_date
        self.status = status
        self.type = type