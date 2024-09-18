from fastapi import APIRouter, Depends, status
from app.core.factories.operation_factory import StandardOperationFactory
from app.application.interfaces.operation_service import OperationService
from app.application.dtos.operation import OperationCreateDTO
from app.external.auth.auth_service import get_current_user
from app.external.api.dependencies import get_json_user_repository, get_json_operation_repository
from app.external.data_access.repositories.json_user_repository import JsonUserRepository
from app.external.data_access.repositories.json_operation_repository import JsonOperationRepository
from app.external.api.schemas.operation import OperationInput, OperationOut, OperationOutDetail
from app.external.auth.exceptions import CredentialsException

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated, Union, List


router = APIRouter(dependencies=[Depends(get_json_user_repository)],
                   prefix="/operation")


@router.post("/create", response_model=OperationOutDetail)
def create_operation(operation_to_create: OperationInput, user_repository: JsonUserRepository = Depends(get_json_user_repository),
                     operation_repository: JsonOperationRepository = Depends(get_json_operation_repository),
                     current_user: dict = Depends(get_current_user)):

    try:
        
        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()
        
        operation_factory = StandardOperationFactory()
        operation_service = OperationService(operation_repository, user_repository)
        new_operation = OperationCreateDTO(
            user_id=operation_to_create.user_id,
            amount=operation_to_create.amount,
            description=operation_to_create.description,
            available_amount=operation_to_create.amount,
            interest_rate=operation_to_create.interest_rate,
            limit_date=operation_to_create.limit_date
        )
        created_operation = operation_service.create_operation(new_operation, operation_factory)
        return created_operation
    
    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/available/", response_model=Union[OperationOut, List[OperationOut]])
def get_all_available_operations(user_repository: JsonUserRepository = Depends(get_json_user_repository),
                     operation_repository: JsonOperationRepository = Depends(get_json_operation_repository),
                     current_user: dict = Depends(get_current_user)):
    
    try:
        
        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()
    
        operation_service = OperationService(operation_repository, user_repository)
        operations = operation_service.get_all_open()
        return operations
    
    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )



@router.get("/{operation_id}", response_model=OperationOutDetail)
def get_detailed_operation_by_id(operation_id: str, user_repository: JsonUserRepository = Depends(get_json_user_repository),
                     operation_repository: JsonOperationRepository = Depends(get_json_operation_repository),
                     current_user: dict = Depends(get_current_user)):
    
    try:
        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()
    
        operation_service = OperationService(operation_repository, user_repository)
        operation = operation_service.get_operation_by_id(operation_id)
        return operation
    
    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        

@router.get("/all/{user_id}", response_model=Union[OperationOutDetail, List[OperationOutDetail]])
def get_all_operation_by_user_id(user_id, user_repository: JsonUserRepository = Depends(get_json_user_repository),
                     operation_repository: JsonOperationRepository = Depends(get_json_operation_repository),
                     current_user: dict = Depends(get_current_user)):
    
    try:
        
        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()
    
        operation_service = OperationService(operation_repository, user_repository)
        operations = operation_service.get_all_operations_by_user_id(user_id)
        return operations
    
    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )



@router.post("/delete")
def delete_operation(operation_id: str, user_id: str, user_repository: JsonUserRepository = Depends(get_json_user_repository),
                     operation_repository: JsonOperationRepository = Depends(get_json_operation_repository),
                     current_user: dict = Depends(get_current_user)) -> str:
    try:
        
        user_email = current_user.get("sub")
        if user_email is None:
            raise CredentialsException()
        
    
        operation_service = OperationService(operation_repository, user_repository)
        operation_was_deleted = operation_service.delete(user_id, operation_id, user_email)
        return JSONResponse(
            content=jsonable_encoder({"msg":"La operacion fue eliminada con exito"}),
            status_code=status.HTTP_204_NO_CONTENT,
        )
    
    except Exception as error:
        return JSONResponse(
            content=jsonable_encoder({"error", f"{error}"}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )