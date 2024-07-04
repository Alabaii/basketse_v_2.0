from typing import Any, List, Union # noqa
from uuid import UUID
from fastapi import  HTTPException
from beanie import PydanticObjectId # noqa
from beanie.operators import In
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
import pymongo
from app.basket.models import MasterDB, Stok, BasketOut, Summary
from app.partner.models import Partner

from app.config.config import Settings
master_db_collection = MasterDB

client = AsyncIOMotorClient(Settings().DATABASE_URL)

async def add_master_db(master_db: List[MasterDB]) -> Any:
    master_db = await MasterDB.insert_many(master_db)
    

stok_collection = Stok
async def add_stok(stok: List[Stok]) -> Any:

    new_stok = await Stok.insert_many(stok)


async def find_basket(basketin):
    partner_list = await client.basketse.partner.find().to_list(None)
    basketout=[]
    ref_list=[]
    for i in range(len(basketin)):
        ref_list.append(basketin[i].dict().get('referenceSku'))
    for partner in partner_list:
        basket=[]
        BasketOut.state = 1
        result = await Stok.find(In(Stok.referencesSku, ref_list)).find(Stok.partner_uuid == partner.get('_id')).to_list()
        BasketOut.partner_uuid = partner.get('_id')
        BasketOut.link = partner.get('link')
        BasketOut.logo = partner.get('logo')
        for i in range(len(result)):
            BasketOut.summary.fullyinstock = 0
            BasketOut.summary.partial = 0
            BasketOut.summary.outofstock =0
            if result[i].dict().get('referencesSku') in ref_list:
                BasketOut.summary.outofstock += len(ref_list) - len(result)
                BasketOut.state =2
            for j in range(len(basketin)):
                if basketin[j].dict().get('referenceSku') == result[i].dict().get('referencesSku'):
                    count = j
            if result[i].dict().get('count') > basketin[count].dict().get('count'):
                    BasketOut.summary.fullyinstock+=1
                    basket=[]
                    basket.append({'referenceSku':result[i].dict().get('referencesSku'), 'count': basketin[count].dict().get('count') })
            else: 
                    BasketOut.summary.partial+=1
                    BasketOut.state = 3
                    basket.append({'referenceSku':result[i].dict().get('referencesSku'), 'count': result[i].dict().get('count') })
            BasketOut.rating = 1
            BasketOut.token = uuid.uuid4()
            BasketOut.id = uuid.uuid4()
            BasketOut.basket = basket
            summ= Summary(fullyinstock=BasketOut.summary.fullyinstock,partial=BasketOut.summary.partial,outofstock=BasketOut.summary.outofstock )
            m = BasketOut(id=BasketOut.id,partner_uuid=BasketOut.partner_uuid,link=BasketOut.link,logo=BasketOut.logo,token=BasketOut.token,basket=BasketOut.basket,state=BasketOut.state, summary=summ ,rating=BasketOut.rating)
            basketout.append(m)
            new_basket=await m.create()


    return basketout