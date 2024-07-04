from uuid import UUID
from fastapi import APIRouter,Depends, HTTPException, status, Body

from app.pagination import Page, Params
from fastapi_paginate.ext.motor import paginate
from motor.motor_asyncio import AsyncIOMotorClient

from app.partner.models import Partner
from app.partner.schemas import Response, UpdatePartnerModel
from app.partner.dao import add_partner, update_partner_data, retrieve_partner, delete_partner #retrieve_partners
from app.config.config import Settings


router = APIRouter(
    prefix="/partner",
    tags = ["Партнёры"]
)

client = AsyncIOMotorClient(Settings().DATABASE_URL)

@router.get("/list",
        response_description="Partners retrieved",
        response_model=Page[Partner])
async def get_partners(
    params : Params = Depends()
    ):
    result = await paginate(client.basketse.partner)
    return result

@router.post(
    "/create",
    response_description="Partner data added into the database",
    response_model=Response,
    status_code=status.HTTP_201_CREATED
)
async def add_partner_data(partner: Partner = Body(...)):
    new_partner = await add_partner(partner)
    partner_id = new_partner.id
    print(partner_id)
    new_conn = client.basketse[f'{partner_id}'].insert_one({"creation_date": "now"})
    return {
        "detail": "Partner created successfully",
        "data": new_partner
    }

@router.put("/{id}", response_model=Response)
async def update_partner(id: UUID, req: UpdatePartnerModel = Body(...)):
    updated_partner = await update_partner_data(id, req.model_dump())
    if not updated_partner:
        raise HTTPException(
            status_code=404,
            detail="Partner id {} not found".format(id),
            headers={"X-Error": "There goes my error"},
        )
    return {
        "detail": "partner information updated",
        "data": updated_partner
    }

@router.get("/{id}", response_description="Partner data retrieved", response_model=Response)
async def get_partner_data(id: UUID):
    partner = await retrieve_partner(id)
    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner id {} not found".format(id),
            headers={"X-Error": "There goes my error"},
        )
    return {
        "detail": "partner information",
        "data": partner
    }

@router.delete("/{id}", response_description="Partner data retrieved", response_model=Response)
async def delete_partner_data(id: UUID):
    partner = await delete_partner(id)
    return {
        "detail": "partner information delete",
        "data": partner
    }