from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from classes.database import get_cursor
from classes import models_orm
import utilities
from sqlalchemy.exc import IntegrityError

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

# endpoint
router= APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# get all orders
@router.get('')
async def list_orders(
    token: Annotated[str, Depends(oauth2_scheme)], 
    cursor: Session = Depends(get_cursor)):
        decoded_client_id = utilities.decode_token(token)
        all_orders = cursor.query(models_orm.Orders).filter(models_orm.Orders.client_id == decoded_client_id).all()
        return all_orders 


class order_post(BaseModel):
    jersey_id:int

# create an order
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_order(
    token: Annotated[str, Depends(oauth2_scheme)], 
    payload:order_post,
    cursor: Session = Depends(get_cursor)
    ):
    decoded_client_id = utilities.decode_token(token)
    new_order= models_orm.Oredrs(client_id=decoded_client_id, jersey_id=payload.jersey_id)
    try : 
        cursor.add(new_order)
        cursor.commit()
        cursor.refresh(new_order)
        return {'message' : f'New order added on {new_order.order_date} with id:{new_order.id}' }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='the given jersey does not exist'
        )