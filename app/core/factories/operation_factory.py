from app.core.interfaces.operations import OperationBaseFactory
from app.core.entities.operation import StandardOperation

class StandardOperationFactory(OperationBaseFactory):

    @classmethod
    def new_operation(self, user_id, description, amount, available_amount, interest_rate, limit_date):
        return StandardOperation(user_id, description, amount, available_amount, interest_rate, limit_date)

