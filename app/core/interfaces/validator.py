from abc import ABC, abstractmethod

class ValidatorBase(ABC):
   """
   Clase base abstracta para validadores.

   Esta clase define la interfaz para implementar validadores
   en el sistema. Las clases concretas que hereden de esta
   deben implementar el método validate.
   """

   @abstractmethod
   def validate(self):
       """
       Método abstracto para realizar validaciones.

       Este método debe ser implementado por las clases hijas para
       proporcionar la lógica específica de validación.

       Raises:
           NotImplementedError: Si este método no es implementado por la clase hija.
       """
       pass
