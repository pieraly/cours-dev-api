from fastapi import APIRouter
from app.schemas_dto import JerseySchema
from app.database import execute_query

router = APIRouter()

@router.get("/jerseys")
async def get_jerseys():
    query = "SELECT * FROM jersey"
    jerseys = execute_query(query)
    return jerseys

@router.post("/jerseys")
async def create_jersey(jersey: JerseySchema):
    query = "INSERT INTO jersey (name, price, tags, stock, availability) VALUES (%s, %s, %s, %s, %s)"
    values = (jersey.name, jersey.price, jersey.tags, jersey.stock, jersey.availability)
    execute_query(query, values)
    return {"message": "New jersey created"}

# Ajoute ici d'autres points de terminaison pour les maillots (mise à jour, suppression, etc.)
