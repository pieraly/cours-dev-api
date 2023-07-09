from fastapi import APIRouter
from app.schemas_dto import UserSchema
from app.database import execute_query

router = APIRouter()

@router.get("/users")
async def get_users():
    query = "SELECT * FROM user"
    users = execute_query(query)
    return users

@router.post("/users")
async def create_user(user: UserSchema):
    query = "INSERT INTO user (name, mdp, email) VALUES (%s, %s, %s)"
    values = (user.name, user.mdp, user.email)
    execute_query(query, values)
    return {"message": "New user created"}

# Ajoute ici d'autres points de terminaison pour les utilisateurs (mise à jour, suppression, etc.)
