from fastapi import APIRouter, Depends, status
from app.core.factories.bid_builder import BidBuilder
from app.application.interfaces.bid_service import BidService
from app.application.dtos.bid import BidCreateDTO
from app.external.auth.auth_service import get_current_user
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
                                 Depends(get_json_operation_repository)],
                   prefix="/bid")


@router.get("/", response_model=Union[BidOut, List[BidOut]])
def get_all_bids_by_user(user_repository: JsonUserRepository = Depends(get_json_user_repository),
                         operation_repository: JsonOperationRepository = Depends(
                             get_json_operation_repository),
                         bid_repository: JsonBidRepository = Depends(
                             get_json_bid_repository),
                         current_user: dict = Depends(get_current_user),
                         event_manager: EventManager = Depends(get_event_manager)):

    try:

        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()

        bid_service = BidService(
            bid_repository, user_repository, operation_repository, event_manager)
        operations = bid_service.get_all_bids_by_user(user_email)
        return operations

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post("/create", response_model=BidOut)
def create_bid(bid_to_create: BidInput,
               user_repository: JsonUserRepository = Depends(
                   get_json_user_repository),
               operation_repository: JsonOperationRepository = Depends(
                   get_json_operation_repository),
               bid_repository: JsonBidRepository = Depends(
                   get_json_bid_repository),
               current_user: dict = Depends(get_current_user)):

    try:

        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()

        bid_builder = BidBuilder()
        new_bid = BidCreateDTO.model_construct(**bid_to_create.model_dump())
        bid_service = BidService(
            bid_repository, user_repository, operation_repository)
        created_bid = bid_service.create_bid(new_bid, bid_builder)
        return created_bid

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/{operation_id}", response_model=Union[BidOut, List[BidOut]])
def get_bids_by_operation_id(operation_id: str, user_repository: JsonUserRepository = Depends(get_json_user_repository),
                             operation_repository: JsonOperationRepository = Depends(
                                 get_json_operation_repository),
                             bid_repository: JsonBidRepository = Depends(
                                 get_json_bid_repository),
                             current_user: dict = Depends(get_current_user)):

    try:

        user_email: EmailStr = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()

        bid_service = BidService(bid_repository=bid_repository,
                                 user_repository=user_repository, operation_repository=operation_repository)
        operations = bid_service.get_bids_by_operation_id(
            operation_id, user_email)
        return operations

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


"""
@router.post("/delete/")
def delete_operation(operation_id: str, user_id: str, user_repository: JsonUserRepository = Depends(get_json_user_repository),
                     operation_repository: JsonOperationRepository = Depends(
                         get_json_operation_repository),
                     current_user: dict = Depends(get_current_user)) -> str:
    try:

        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()

        operation_service = OperationService(
            operation_repository, user_repository)
        operation_was_deleted = operation_service.delete(
            user_id, operation_id, user_email)
        return JSONResponse(
            content=jsonable_encoder(
                {"msg": "La operacion fue eliminada con exito"}),
            status_code=status.HTTP_204_NO_CONTENT,
        )

    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )"""
