from app.application.interfaces.event_manager import EventManagerBase



class EventManager(EventManagerBase):
    observers = {}
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def subscribe(cls, event_type, observer):
        if event_type not in cls.observers:
            cls.observers[event_type] = []
        cls.observers[event_type].append(observer)
        return True

    @classmethod
    def notify(cls, event_type, data):
        if event_type in cls.observers:
            for observer in cls.observers[event_type]:
                observer.update(event_type, data)
        return True
