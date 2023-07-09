from pydantic import BaseModel

# Schéma DTO pour les maillots
class JerseySchema(BaseModel):
    name: str
    price: float
    tags: str
    availability: bool = True
    stock: int = None

# Schéma DTO pour les utilisateurs
class UserSchema(BaseModel):
    name: str
    mdp: int
    email: str

# Schéma DTO pour les transactions
class TransactionSchema(BaseModel):
    user_id: int
    jersey_id: int
    timestamp: str
    quantity: int
    total_amount: float
