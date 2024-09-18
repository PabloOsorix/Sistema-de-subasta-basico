from app.application.events.event_manager import EventManager
from app.external.data_access.repositories.json_user_repository import JsonUserRepository
from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository
from app.external.data_access.repositories.json_bid_repository import JsonBidRepository
from fastapi import Depends
from typing import Annotated

def get_json_user_repository():
    return JsonUserRepository()

def get_json_operation_repository():
    return JsonOperationRepository()

def get_json_bid_repository():
    return JsonBidRepository()

def get_event_manager():
    return EventManager._instance
