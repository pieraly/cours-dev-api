from fastapi import FastAPI # depuis le package fastapi import la classe fastapi
app = FastAPI() #nom de variables pour les servers

@app.get("/test")
async def root(): # le port sera définit automatiquement sur 8000
    return {"message": "bien vu poto"}