from fastapi import APIRouter, Depends, status
from app.core.factories.bid_builder import BidBuilder
from app.application.interfaces.bid_service import BidService
from app.application.dtos.bid import BidCreateDTO
from app.external.auth.auth_service import get_current_user, verify_user
from app.external.api.dependencies import (
    get_json_user_repository,
    get_json_operation_repository,
    get_json_bid_repository,
    get_event_manager
)
from app.external.data_access.repositories.json_user_repository import JsonUserRepository
from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository
from app.external.data_access.repositories.json_bid_repository import JsonBidRepository
from app.external.api.schemas.bid import BidInput, BidOut
from app.external.auth.exceptions import CredentialsException
from app.application.events.event_manager import EventManager

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Union, List
from pydantic import EmailStr


router = APIRouter(dependencies=[Depends(get_json_user_repository),
                                 Depends(get_json_bid_repository),
                                 Depends(get_json_operation_repository),
                                 Depends(get_current_user),
                                 Depends(verify_user)],
                   prefix="/bid")

def repositories(operation_repository: JsonOperationRepository = Depends(get_json_operation_repository),
                      user_repository: JsonUserRepository = Depends(get_json_user_repository),
                      bid_repository: JsonBidRepository = Depends(get_json_bid_repository)):
    return {"operation": operation_repository, "user": user_repository, "bid": bid_repository}

repositoriesDep = Annotated[dict, Depends(repositories)]




@router.post("/create", response_model=BidOut)
def create_bid(bid_to_create: BidInput, repositories: repositoriesDep,
               event_manager: EventManager = Depends(get_event_manager)):

    try:

        bid_builder = BidBuilder()
        new_bid = BidCreateDTO.model_construct(**bid_to_create.model_dump())
        bid_service = BidService(
            repositories["bid"], repositories["user"], repositories["operation"], event_manager)
        created_bid = bid_service.create_bid(new_bid, bid_builder)
        return created_bid

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/", response_model=Union[BidOut, List[BidOut]])
def get_all_bids_by_user(repositories: repositoriesDep, event_manager: EventManager = Depends(get_event_manager),
                         current_user_email: str = Depends(verify_user)):

    try:

        bid_service = BidService(
            repositories["bid"], repositories["user"], repositories["operation"], event_manager)
        operations = bid_service.get_all_bids_by_user(email=current_user_email)
        return operations

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )



@router.get("/{operation_id}", response_model=Union[BidOut, List[BidOut]])
def get_bids_by_operation_id(operation_id: str, repositories: repositoriesDep,
                             event_manager: EventManager = Depends(get_event_manager),
                             current_user_email: str = Depends(verify_user)):

    try:

        bid_service = BidService(bid_repository=repositories["bid"],
                                 user_repository=repositories["user"],
                                 operation_repository=repositories["operation"],
                                 event_manager=event_manager
                                 )
        operations = bid_service.get_bids_by_operation_id(
            operation_id, current_user_email)
        return operations

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )