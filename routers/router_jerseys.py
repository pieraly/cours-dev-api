from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm, schemas_dto

router = APIRouter(
    prefix='/jerseys',
    tags=['Jerseys']
)

# Read
@router.get('')
async def get_jerseys(
    cursor: Session= Depends(get_cursor), 
    limit:int=10, offset:int=0):
    all_jerseys = cursor.query(models_orm.Jerseys).limit(limit).offset(offset).all() # Lancement de la requête
    jerseys_count= cursor.query(func.count(models_orm.Jerseys.jersey_id)).scalar()
    return {
        "products": all_jerseys,
        "limit": limit,
        "total": jerseys_count,
        "skip":offset
    }

# Read by id
@router.get('/{jersey_id}', response_model=schemas_dto.Jersey_GETID_Response)
async def get_jersey(jersey_id:int, cursor:Session= Depends(get_cursor)):
    corresponding_jersey = cursor.query(models_orm.Jerseys).filter(models_orm.Jerseys.jersey_id == jersey_id).first()
    if(corresponding_jersey):  
        return corresponding_jersey
    else:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding product found with id : {jersey_id}"
        )

# CREATE / POST 
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_jersey(payload: schemas_dto.Jersey_POST_Body, cursor:Session= Depends(get_cursor)):
    new_jersey = models_orm.Jerseys(name=payload.name,price= payload.price,tags= payload.tags,stock= payload.stock,availability= payload.availability) # build the insert
    cursor.add(new_jersey) 
    cursor.commit() 
    cursor.refresh(new_jersey)
    return {"message" : f"New Jersey {new_jersey.name} added sucessfully with id: {new_jersey.jersey_id}"} 

# DELETE 
@router.delete('/{jersey_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_jersey(jersey_id:int, cursor:Session=Depends(get_cursor)):
    corresponding_jersey = cursor.query(models_orm.Jerseys).filter(models_orm.Jerseys.jersey_id == jersey_id)
    if(corresponding_jersey.first()):
        corresponding_jersey.delete() 
        cursor.commit() 
        return
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ne corresponding product with id: {jersey_id}'
        )
        
# Update
@router.patch('/{jersey_id}')
async def update_product(jersey_id: int, payload:schemas_dto.Jersey_PATCH_Body, cursor:Session=Depends(get_cursor)):
    corresponding_jersey = cursor.query(models_orm.Jerseys).filter(models_orm.Jerseys.jersey_id == jersey_id)
    if(corresponding_jersey.first()):
        corresponding_jersey.update(
            {"stock": payload.newstock}
        )
        cursor.commit()
        return corresponding_jersey.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding product with id: {jersey_id}'
        )