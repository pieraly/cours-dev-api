from fastapi import APIRouter
from app.schemas_dto import TransactionSchema
from app.database import execute_query

router = APIRouter()

@router.get("/transactions")
async def get_transactions():
    query = "SELECT * FROM transaction"
    transactions = execute_query(query)
    return transactions

@router.post("/transactions")
async def create_transaction(transaction: TransactionSchema):
    query = "INSERT INTO transaction (user_id, jersey_id, timestamp, quantity, total_amount) VALUES (%s, %s, %s, %s, %s)"
    values = (transaction.user_id, transaction.jersey_id, transaction.timestamp, transaction.quantity, transaction.total_amount)
    execute_query(query, values)
    return {"message": "New transaction created"}

# Ajoute ici d'autres points de terminaison pour les transactions (mise à jour, suppression, etc.)
