from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

# classe jersey
class Jersey(BaseModel):
    jersey_id: int
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

# class users
class User(BaseModel):
    name: str
    mdp: int
    email: str

userList = [
    {"user_id": 1, "name": "Steph", "mdp": 123, "email": "steph@example.com"},
    {"user_id": 2, "name": "Imrane", "mdp": 222, "email": "imrane@example.com"},
    {"user_id": 3, "name": "Mondestin", "mdp": 333, "email": "mondestin@example.com"}
]


 # Récupère la liste de tous les maillots 

@app.get("/jerseys")
async def get_jerseys(): 
    
    return {
        "jersey": jerseyList,
        "limit": 10,
        "total": len(jerseyList),  # Nombre total de maillots
        "skip": 0
    }


# Crée un nouveau maillot.

@app.post("/jerseys")
async def create_jersey(payload: Jersey, response: Response):
       
    jerseyList.append(payload.dict())
    response.status_code = status.HTTP_201_CREATED
    return {"message": f"New jersey added successfully: {payload.name}"}


 # Récupère un maillot spécifique en fonction de son ID.

@app.get("/jerseys/{jersey_id}")
async def get_jersey(jersey_id: int, response: Response):
        
    try:
        corresponding_jersey = jerseyList[jersey_id - 1]
        return corresponding_jersey
    except: 
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found"
        )


# Supprime un maillot spécifique en fonction de son ID

@app.delete("/jerseys/{jersey_id}")
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

@app.put("/jerseys/{jersey_id}")
async def replace_jersey(jersey_id: int, payload: Jersey, response: Response):
    
    try:
        corresponding_jersey = jerseyList[jersey_id - 1] = payload.dict()
        return {"message": f"Jersey updated successfully: {payload.name}"}
    except:
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found"
        )
        
        
        
# Récupère la liste de tous les utilisateurs
@app.get("/users")
async def get_users():
    return userList

# Récupère un utilisateur spécifique en fonction de son ID
@app.get("/users/{user_id}")
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
@app.post("/users")
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

@app.put("/users/{user_id}")
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
@app.delete("/users/{user_id}")
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