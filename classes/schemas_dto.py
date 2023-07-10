from pydantic import BaseModel
from datetime import datetime



class Jersey_POST_Body (BaseModel):
    name: str
    price: float
    tags: str
    stock: int
    availability: bool
    
class Jersey_PATCH_Body (BaseModel):
    newstock: int
class Jersey_GETID_Response(BaseModel):
    name: str
    price: float
    tags: str
    availability: bool = True
    stock: int = None
    class Config :
        orm_mode = True

class Client_POST_Body (BaseModel):
    clientEmail:str
    clientPassword: str

class Client_response (BaseModel): 
    client_id: int
    email:str
    
    
    class Config:
        orm_mode= True      
        


