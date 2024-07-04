from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from beanie import Document
from pydantic import Field, HttpUrl





class Partner(Document):
    id : UUID = Field(default_factory = uuid4)
    name : str
    partner_uuid : UUID
    login : str
    link : HttpUrl
    logo: Optional[str] = None
    issue : bool = Field(default = True) # true - true есть в выдаче, false нет в выдаче
    is_delete: bool = Field(default= False) # true - удалено, false активно
    last_seen: datetime = Field(default_factory=datetime.now)
    creation_date: datetime = Field(default_factory=datetime.now)



    class Settings:
        name = "partner"
















# from datetime import datetime
# from pydantic import BaseModel, Field





# class Partner(BaseModel):
#     id : str = Field(alias='_id')
#     name : str
#     partner_uuid : str
#     login : str
#     link : str
#     logo: str
#     issue : bool # true - true есть в выдаче, false нет в выдаче
#     is_delete: bool # true - удалено, false активно
#     creation_date: datetime


