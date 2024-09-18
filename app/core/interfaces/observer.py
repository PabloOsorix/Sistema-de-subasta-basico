from abc import ABC, abstractmethod

class ObserverBase(ABC):
    @abstractmethod
    def update(self, event_type:str, data: dict, Repository):
        """Método que debe implementar cualquier observador para manejar eventos"""
        pass