from fastapi import APIRouter, HTTPException, status, Depends
from classes import schemas_dto, database, models_orm
from sqlalchemy.orm import Session
import utilities

# Formulaire de lancement du OAuth /auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


#endpoint
router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)

#create authentification
@router.post('', status_code=status.HTTP_201_CREATED)
async def auth_client(
        payload : OAuth2PasswordRequestForm= Depends(), 
        cursor: Session= Depends(database.get_cursor)
    ):
    print(payload.__dict__)
    
    # Recupère les crédentials
    corresponding_client = cursor.query(models_orm.Clients).filter(models_orm.Clients.email == payload.username).first()
    
    # Vérifie dans la DB si client exist
    if(not corresponding_client):
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail='wrong email'
         )
    # Vérifie sur password hashé 
    valid_pwd = utilities.verify_password(
        payload.password,
        utilities.hash_password(payload.password)
     )
    if(not valid_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='wrong password' 
        ) 
    # Génération du JWT
    token = utilities.generate_token(corresponding_client.client_id)
    print(token)
    return token