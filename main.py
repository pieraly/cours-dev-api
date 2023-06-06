from argparse import OPTIONAL
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status # depuis le package fastapi import la classe fastapi
from pydantic import BaseModel # lien et vérification
app = FastAPI() #nom de variables pour les servers

# Data Model / schema / DTO
class Jersey(BaseModel):
    name: str
    price: float
    tags: str
    availability: bool = True 
    # stock: int = OPTIONAL   
    stock: Optional[int] # completement optionnel 
    
jersey = [
    {"jersey_id":1,"name": "vinicius", "price": 100 , "tags":"Jr7"},
    {"jersey_id":2,"name": "kaka", "price": 80, "tags": "kaka"},
    {"jersey_id":3,"name": "mitroglou", "price": 50, "tags": "M9"}
]

@app.get("/test")
async def root(): # le port sera définit automatiquement sur 8000
    return {"message": "bien vu poto"}

@app.get("/jersey")
async def root(): 
    return jersey

# @app.get("/jerseyLuxe")
# async def getJersey(): 
#     return {
#         "jersey": [
#             {"name":"Cristiano Ronaldo","tags":"CR7", "club":"Al-Nasser", "price":100},
#             {"name":"Lionel Messi","tags":"LM10","club":" ", "price":100}
#         ],
#         "limit":10,
#         "total": 2,
#         "skip":0
#     }
    
# @app.post("/jersey")
# async def create_post(payload:dict = Body):
#     print(payload["jersey"])
#     return {"message": "New jersey of {jersey} ".format(jersey= payload["jersey"][0]['name'])}

@app.post("/jerseys")
async def create_post(payload: Jersey, response: Response):
    jersey.append(payload.dict())
    response.status_code = status.HTTP_201_CREATED
    print(payload.name)
    return {"message": f"New jersey add succesfuly: {payload.name}"}

@app.get("/jerseys/{jersey_id}")
async def get_jersey(jersey_id: int, response: Response):
    try:
        corresponding_jersey = jersey[jersey_id - 1] # un id commence à 1 alors qu'un tableau commence par 0
        return corresponding_jersey
    except: 
        raise HTTPException (
            status.HTTP_404_NOT_FOUND,
            detail= "Jersey not found"
        )
    