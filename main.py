from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

# import necessaire pour la connexion a la base de donnée
import psycopg2
from psycopg2.extras import RealDictCursor

# connection DB
connexion = psycopg2.connect(
    host = "localhost",
    database = "jerseys",
    user = "postgres",
    password = "root",
    cursor_factory=RealDictCursor
    
)
cursor =  connexion.cursor() #TODO a modifier


# description
api_description = description = """
THis API is built with fatsAPI : 

## Jerseys
    You will be able to :

* Create new jersey
* Get jerseys list
* Update jersey
* Delete jersey

## Users
    You will be able to :

* Create new user
* Get users list
* Update user
* Delete user

"""

# liste des tags utilises dans la doc
tags_metadata = [
    {
        "name": "Users",
        "description": "manage Users "
    },
    {
        "name": "Jerseys",
        "description": "Find the jersey that you want ",
        "externaldocs": {
            
        }
        
    }
    
]

app = FastAPI( title= "Jersey API",
    description=api_description,
    openapi_tags=tags_metadata # tagsmetadata est definit au dessus 
)


#### classes  ####

# jersey #
class Jersey(BaseModel):
    name: str
    price: float
    tags: str
    availability: bool = True 
    stock: Optional[int] = None  # Stock est un champ optionnel

jerseyList = [
    {"jersey_id":1,"name": "vinicius", "price": 100 , "tags":"Jr7", "availability":1, "stock": 150 },
    {"jersey_id":2,"name": "kaka", "price": 80, "tags": "kaka", "availability":0, "stock": 0},
    {"jersey_id":3,"name": "mitroglou", "price": 50, "tags": "M9", "availability":1, "stock": 200}
]

# users #
class User(BaseModel):
    name: str
    mdp: int
    email: str

userList = [
    {"user_id": 1, "name": "Steph", "mdp": 123, "email": "steph@example.com"},
    {"user_id": 2, "name": "Imrane", "mdp": 222, "email": "imrane@example.com"},
    {"user_id": 3, "name": "Mondestin", "mdp": 333, "email": "mondestin@example.com"}
]

#####    #######

 # Récupère la liste de tous les maillots 

@app.get("/jerseys", tags= ["Jerseys"])
async def get_jerseys(): 
    #requete sql
    cursor.execute ("SELECT * FROM jersey")
    dbJerseys = cursor.fetchall()
    return {
        "jersey": dbJerseys,
        "limit": 10,
        "total": len(dbJerseys),  # Nombre total de maillots
        "skip": 0
    }


# Crée un nouveau maillot.
# insert into jersey values ()

@app.post("/jerseys" , tags= ["Jerseys"])
async def create_jersey(payload: Jersey, response: Response):
    cursor.execute(f"INSERT INTO jersey (name, price, tags, stock, availability) VALUES ('{payload.name}',{payload.price}, '{payload.tags}',{payload.stock},'{payload.availability}') RETURNING *;")
    connexion.commit()
   
    response.status_code = status.HTTP_201_CREATED
    return {"message": f"New jersey added successfully: {payload.name}"}


 # Récupère un maillot spécifique en fonction de son ID.

@app.get("/jerseys/{jersey_id}", tags= ["Jerseys"])
async def get_jersey(jersey_id: int, response: Response):
        
    try:
        cursor.execute(f"SELECT * FROM jersey WHERE jersey_id={jersey_id}")
        corresponding_jersey = cursor.fetchone()
        if (corresponding_jersey):
            return corresponding_jersey 
        else:
            raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found")
            
    except: 
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found"
        )


# Supprime un maillot spécifique en fonction de son ID

@app.delete("/jerseys/{jersey_id}" , tags= ["Jerseys"])
async def delete_jersey(jersey_id: int, response: Response):
    
    try:
        jerseyList.pop(jersey_id - 1)
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except:
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found"
        )

# Remplace un maillot existant par un nouveau maillot

@app.put("/jerseys/{jersey_id}", tags= ["Jerseys"])
async def replace_jersey(jersey_id: int, payload: Jersey, response: Response):
    
    try:
        corresponding_jersey = jerseyList[jersey_id - 1] = payload.dict()
        return {"message": f"Jersey updated successfully: {payload.name}"}
    except:
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found"
        )
        
###################################################        
        
# Récupère la liste de tous les utilisateurs
@app.get("/users",  tags= ["Users"])
async def get_users():
    return userList

# Récupère un utilisateur spécifique en fonction de son ID
@app.get("/users/{user_id}", tags= ["Users"])
async def get_user(user_id: int, response: Response):
    try:
        corresponding_user = next(user for user in userList if user["user_id"] == user_id)
        return corresponding_user
    except StopIteration:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

# Crée un nouvel utilisateur
@app.post("/users" ,  tags= ["Users"])
async def create_user(payload: User, response: Response):
    new_user = {
        "user_id": len(userList) + 1,
        "name": payload.name,
        "mdp": payload.mdp,
        "email": payload.email
    }
    userList.append(new_user)
    response.status_code = status.HTTP_201_CREATED
    return {"message": f"New user added successfully: {payload.name}"}

# Met à jour un utilisateur existant

@app.put("/users/{user_id}",  tags= ["Users"])
async def update_user(user_id: int, payload: User, response: Response):
    try:
        index = next(index for index, user in enumerate(userList) if user["user_id"] == user_id)
        userList[index]["name"] = payload.name
        userList[index]["mdp"] = payload.mdp
        userList[index]["email"] = payload.email
        return {"message": f"User updated successfully: {payload.name}"}
    except StopIteration:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )



# Supprime un utilisateur spécifique en fonction de son ID
@app.delete("/users/{user_id}",  tags= ["Users"])
async def delete_user(user_id: int, response: Response):
    try:
        index = next(index for index, user in enumerate(userList) if user["user_id"] == user_id)
        userList.pop(index)
        response.status_code = status.HTTP_204_NO_CONTENT
        return
    except StopIteration:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )