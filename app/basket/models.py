from typing import Optional,List,ClassVar
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document
from pydantic import Field,BaseModel
from pydantic_core import Url


class MasterDB(Document):
    id: str | int
    desc: str
    line : str
    img : Optional[str] = None
    creation_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "masterdb"

class Stok(Document):
    referencesSku: str
    partner_uuid: UUID
    desc: str
    line : str
    img : Optional[str] = None
    count: int
    creation_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "stok"

class Summary(BaseModel):
    fullyinstock: int = 0
    partial: int = 0 
    outofstock: int = 0

class BasketIn(BaseModel):
    referenceSku: str
    count:int


class BasketOut(Document):
    id: UUID
    partner_uuid: UUID
    link: Url
    logo: str
    token: UUID = Field(default_factory = uuid4)
    basket : List[BasketIn]
    state: int
    summary: Summary | None = None
    rating: int = 1
    class Settings:
        name = "basketout"