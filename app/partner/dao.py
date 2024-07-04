from typing import Any, List, Union # noqa
from uuid import UUID
from fastapi import  HTTPException
from beanie import PydanticObjectId # noqa

from app.partner.models import Partner

partner_collection = Partner


async def add_partner(new_partner: Partner) -> Partner:
    partner = await new_partner.create()
    
    return partner

async def update_partner_data(id: UUID, data: dict) -> Union[bool, Partner]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    partner = await partner_collection.get(id)
    if partner:
        await partner.update(update_query)
        return partner
    return False

async def retrieve_partner(id: UUID) -> Partner:
    partner = await partner_collection.get(id)
    if partner:
        return partner

async def delete_partner(id: UUID) -> Any:
    partner_to_delete = await Partner.get(id)
    if not partner_to_delete:
        raise HTTPException(
            status_code=404,
            detail="Partner id {} not found".format(id),
            headers={"X-Error": "There goes my error"},
        )
    await partner_to_delete.delete()

# async def retrieve_partners() -> Any:
#     partners = await partner_collection.all().to_list()
#     return partners

