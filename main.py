from fastapi import FastAPI
from classes.database import database_engine

import classes.models_orm
import routers.router_jerseys, routers.router_client, routers.router_auth, routers.router_orders

from documentation.description import api_description
from documentation.tags import tags_metadata

app= FastAPI( 
    title="Jerseys API",
    description=api_description,
    openapi_tags=tags_metadata 
    )


classes.models_orm.Base.metadata.create_all(bind=database_engine)

app.include_router(routers.router_jerseys.router)
app.include_router(routers.router_client.router)
app.include_router(routers.router_orders.router)
app.include_router(routers.router_auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Jersey API!"}
