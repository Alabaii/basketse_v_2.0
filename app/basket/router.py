from typing import Any, List
from uuid import UUID
from fastapi import APIRouter,Depends, HTTPException, status, Body

from app.pagination import Page, Params
from fastapi_paginate.ext.motor import paginate
from motor.motor_asyncio import AsyncIOMotorClient

from app.basket.models import MasterDB, Stok,BasketIn, BasketOut
from app.partner.schemas import Response, UpdatePartnerModel
from app.basket.dao import add_master_db, add_stok, find_basket #update_partner_data, retrieve_partner, delete_partner #retrieve_partners
from app.config.config import Settings


router = APIRouter(
    prefix="/basket",
    tags = ["Корзина"]
)

client = AsyncIOMotorClient(Settings().DATABASE_URL)


@router.post(
    "/upload-master_db",
    response_description="master database has been loaded",
    response_model=Response,
    status_code=status.HTTP_201_CREATED
)
async def upload_master_db(master_db: List[MasterDB] = Body(...)):
    new_master_db = await add_master_db(master_db)
    return {
        "detail": "master database has been loaded",
        "data": new_master_db
    }

@router.post(
    "/upload-stok",
    response_description="stok has been loaded",
    response_model=Response,
    status_code=status.HTTP_201_CREATED
)
async def upload_stok(stok: List[Stok] = Body(...)):
    new_stok = await add_stok(stok)
    return {
        "detail": "stok has been loaded",
        "data": new_stok
    }

@router.post(
    "/create",
    response_description="the basket is formed",
    response_model=Response,
    status_code=status.HTTP_201_CREATED
)
async def create_basket(basketin: List[BasketIn]= Body(...)) -> List[BasketOut]:
    result = await find_basket(basketin)
    
    return {
        "detail": "the basket is formed",
        "data": result
    }
