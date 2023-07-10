from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from classes import models_orm, schemas_dto, database
import utilities
from typing import List

#endpoint
router = APIRouter(
    prefix='/clients',
    tags=['Clients']
)

#create new client
@router.post('', response_model=schemas_dto.Client_response, status_code= status.HTTP_201_CREATED)
async def create_client(
    payload: schemas_dto.Client_POST_Body, 
    cursor: Session = Depends(database.get_cursor),
    ):
    try: 
        
        hashed_password = utilities.hash_password(payload.clientPassword) 
        
        new_client= models_orm.Clients(password=hashed_password, email= payload.clientEmail)
     
        cursor.add(new_client) 
       
        cursor.commit() 
       
        cursor.refresh(new_client) 
        return new_client 
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Client already exists" 
        )

# get all client 
@router.get('', response_model=List[schemas_dto.Client_response])
async def get_all_clients(cursor: Session = Depends(database.get_cursor)):
    all_clients = cursor.query(models_orm.Clients).all()
    return all_clients

# get one specific client
@router.get('/{client_id}', response_model=schemas_dto.Client_response)
async def get_user_by_id(client_id:int, cursor: Session = Depends(database.get_cursor)):
    corresponding_client = cursor.query(models_orm.Clients).filter(models_orm.Clients.client_id == client_id).first()
    if(corresponding_client):
        return corresponding_client
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No client with id:{client_id}'
        )