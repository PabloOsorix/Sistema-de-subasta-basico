from app.external.data_access.interfaces.operation import OperationDbBase




class OperationJsonEntity(OperationDbBase):
    def __init__(self, id: str, user_id: str, description: str, amount: str, interest_rate: str, limit_date: str, status: str, create_date: str, type: str, available_amount: int|str) -> None:
        super().__init__(id, user_id, description, amount, interest_rate, limit_date, status, create_date, type, available_amount)

