from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.config import Settings,initiate_database

from fastapi_paginate import add_pagination




from app.partner.router import router as router_partner
from app.basket.router import router as router_basket


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    global client
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await initiate_database(client=client)



app.include_router(router_partner)
app.include_router(router_basket)



add_pagination(app)
