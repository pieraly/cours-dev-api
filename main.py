from fastapi import FastAPI
from classes.database import Base, engine
from routers import jerseys, users, transactions

app = FastAPI()

# Effectue les opérations de migration de la base de données
Base.metadata.create_all(bind=engine)

app.include_router(jerseys.router)
app.include_router(users.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Jersey API!"}
