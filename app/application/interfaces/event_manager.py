from abc import ABC


class EventManagerBase(ABC):
    """
    Class: EventManagerBase
    Define los métodos base para la gestión de eventos y suscriptores.
    """

    @classmethod
    def subscribe(cls, event_type, observer):
        """
        Method: subscribe
        Suscribe un observador a un tipo de evento.

        Args:
            event_type (str): El tipo de evento al que suscribir el observador.
            observer (Observer): El observador que se suscribe al evento.
        """
        pass

    @classmethod
    def notify(cls, event_type, data):
        """
        Method: notify
        Notifica a todos los observadores suscritos a un tipo de evento.

        Args:
            event_type (str): El tipo de evento que se ha activado.
            data (dict): Datos relacionados con el evento que se notifica.
        """
        pass