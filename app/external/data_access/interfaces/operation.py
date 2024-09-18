from abc import ABC

class OperationDbBase(ABC):
    def __init__(self, id, user_id, description, amount, interest_rate, limit_date, status, create_date, type, available_amount: str | int) -> None:
        self.id = id
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.available_amount = available_amount
        self.interest_rate = interest_rate
        self.limit_date = limit_date
        self.status = status
        self.create_date = create_date
        self.type = type


