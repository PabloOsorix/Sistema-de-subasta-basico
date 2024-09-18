
from datetime import date, datetime
from app.core.interfaces.validator import ValidatorBase

class AmountValidator(ValidatorBase):
    """
    Class: AmountValidator
    Valida que el monto de la operación no sea negativo.
    """

    @staticmethod
    def validate(amount) -> int:
        """
        Method: validate
        Valida que el monto no sea negativo.

        Args:
            amount (int): El monto a validar.

        Raises:
            ValueError: Si el monto es negativo.

        Returns:
            int: El monto validado como entero.
        """
        if amount < 0:
            raise ValueError("El monto de la operacion no puede ser negativo")
        return int(amount)

        
        
class InterestRateValidator(ValidatorBase):
    """
    Class: InterestRateValidator
    Valida que la tasa de interés esté dentro de los límites permitidos según el sistema financiero peruano.
    """

    @staticmethod
    def validate(interest_rate):
        """
        Metodo que
        convierte la tasa de interés a flotante y verifica que esté dentro del rango permitido.

        Args:
            interest_rate (float): La tasa de interés a validar.

        Raises:
            ValueError: Si la tasa de interés no está dentro del rango permitido.

        Returns:
            float: La tasa de interés validada.
        """
        try:
            interest_rate = float(interest_rate)
            if interest_rate <= 0.0 or interest_rate >= 30.0:
                raise ValueError("La tasa de interes no puede ser menor al 0% o mayor al 30% segun el sistema financiero peruano")
            return interest_rate
        except:
            raise        
        

class InterestRateValidationByOperation(InterestRateValidator):
    """
    Class: InterestRateValidationByOperation
    Valida que la tasa de interés propuesta no supere la tasa fijada en la operación.
    """

    @staticmethod
    def validate(cls, interest_rate: float, operation_interest_rate: float):
        """
        Method que
        Valida que la tasa de interés propuesta esté dentro del rango y no supere la tasa de la operación.

        Args:
            interest_rate (float): La tasa de interés propuesta.
            operation_interest_rate (float): La tasa de interés de la operación.

        Raises:
            ValueError: Si la tasa de interés propuesta supera la de la operación o está fuera de rango.
        """
        try:
            interest_rate = super().validate(interest_rate)
            if interest_rate > operation_interest_rate:
                raise ValueError("La tasa de interes propuesta no puede ser mayor a la fijada en la operacion")
        except ValueError:
            raise


class LimitDateValidator(ValidatorBase):
    """
    Class: LimitDateValidator
    Valida que la fecha límite esté en el formato correcto y no sea anterior a la fecha actual.
    """

    @staticmethod
    def validate(limit_date):
        """
        Metodo que
        Valida que la fecha límite esté en el formato correcto y sea posterior al día actual.

        Args:
            limit_date (str): La fecha límite a validar en formato 'YYYY-MM-DD'.

        Raises:
            ValueError: Si la fecha está en formato incorrecto o es anterior o igual al día actual.

        Returns:
            datetime: La fecha límite validada.
        """
        
        
        format = "%Y-%m-%d"
        try:
            limit_date = datetime.strptime(limit_date, format)
            if limit_date is None:
                raise ValueError("La fecha limite no puede ser nula")
            elif limit_date.date() <= datetime.now().date():
                raise ValueError("La fecha limite no puede ser igual o menor al dia actual")
            return limit_date
        except Exception as error:
            if "does not match format" in error.__str__():
                raise Exception(f"El formato de fecha es incorrecto. Se espera {format}")
            raise Exception(f"{error}")
    