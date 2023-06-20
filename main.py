from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

# Connexion à la base de données
connexion = psycopg2.connect(
    host="dpg-ci8rmv18g3n3vm6clj9g-a.frankfurt-postgres.render.com",
    database="jerseys",
    user="steph_render",
    password="ZIPWG5kTQqhuqrLWtZLQWAg08VLD2MHY",
    cursor_factory=RealDictCursor
)
cursor = connexion.cursor()


# Description
api_description = """
This API is built with FastAPI:

## Jerseys
You will be able to:
* Create a new jersey
* Get the list of jerseys
* Update a jersey
* Delete a jersey

## Users
You will be able to:
* Create a new user
* Get the list of users
* Update a user
* Delete a user
"""

tags_metadata = [
    {
        "name": "Users",
        "description": "Manage Users"
    },
    {
        "name": "Jerseys",
        "description": "Find the jersey you want"
    }
]

app = FastAPI(
    title="Jersey API",
    description=api_description,
    openapi_tags=tags_metadata
)


# Jersey
class Jersey(BaseModel):
    name: str
    price: float
    tags: str
    availability: bool = True
    stock: Optional[int] = None

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


@app.get("/jerseys", tags=["Jerseys"])
async def get_jerseys():
    cursor.execute("SELECT * FROM jersey")
    db_jerseys = cursor.fetchall()
    return {
        "jersey": db_jerseys,
        "limit": 10,
        "total": len(db_jerseys),
        "skip": 0
    }


@app.post("/jerseys", tags=["Jerseys"])
async def create_jersey(payload: Jersey, response: Response):
    cursor.execute(
        "INSERT INTO jersey (name, price, tags, stock, availability) VALUES (%s,%s,%s,%s,%s) RETURNING *;",
        (payload.name, payload.price, payload.tags, payload.stock, payload.availability)
    )
    connexion.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"message": f"New jersey added successfully: {payload.name}"}


@app.get("/jerseys/{jersey_id}", tags=["Jerseys"])
async def get_jersey(jersey_id: int, response: Response):
    try:
        cursor.execute(f"SELECT * FROM jersey WHERE jersey_id={jersey_id}")
        corresponding_jersey = cursor.fetchone()
        if corresponding_jersey:
            return corresponding_jersey
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Jersey not found"
            )
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found"
        )


@app.delete("/jerseys/{jersey_id}", tags=["Jerseys"])
async def delete_jersey(jersey_id: int, response: Response):
    try:
        cursor.execute("DELETE FROM jersey WHERE jersey_id = %s", (jersey_id,))
        connexion.commit()
        response.status_code = status.HTTP_202_ACCEPTED
        return  {"message": "Jersey deleted"}
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Jersey not found"
        )



@app.put("/jerseys/{jersey_id}", tags=["Jerseys"])
async def replace_jersey(jersey_id: int, payload: Jersey, response: Response):
    cursor.execute(f"SELECT * FROM jersey WHERE jersey_id={jersey_id}")
    corresponding_jersey = cursor.fetchone()
    
    if corresponding_jersey is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="ID not found"
        )
    
    try:
        cursor.execute(
            "UPDATE jersey SET name = %s, price = %s, tags = %s, stock = %s, availability = %s WHERE jersey_id = %s",
            (payload.name, payload.price, payload.tags, payload.stock, payload.availability, jersey_id)
        )
        connexion.commit()
        return {"message": "Jersey updated"}
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update jersey"
        )


# User
class User(BaseModel):
    name: str
    mdp: int
    email: str


@app.get("/users", tags=["Users"])
async def get_users():
    return userList


@app.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: int, response: Response):
    try:
        corresponding_user = next(user for user in userList if user["user_id"] == user_id)
        return corresponding_user
    except StopIteration:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@app.post("/users", tags=["Users"])
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


@app.put("/users/{user_id}", tags=["Users"])
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


@app.delete("/users/{user_id}", tags=["Users"])
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
