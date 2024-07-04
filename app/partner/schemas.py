from pydantic import BaseModel, HttpUrl
from typing import Optional, Any

class UpdatePartnerModel(BaseModel):
    name : Optional[str] = None
    partner_uuid : Optional[str] = None
    login : Optional[str] = None
    link : Optional[HttpUrl] = None
    logo: Optional[str] = None
    issue : Optional[bool] = None # true - true есть в выдаче, false нет в выдаче

    class Collection:
        name = "partner"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "company name",
                "partner_uuid": "uuid issued by se",
                "login": "company login",
                "link": "https://example_company.com/api",
                "logo": "picture link",
                "issue": True
            }
        }

class Response(BaseModel):
    detail: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Some detail",
                "data": "Sample data",
            }
        }











# def ResponseSchema(message, data):
#     return {
#         "detail": message,
#         "code": 200,
#         "data": [data]
#     }

# def individual_serial(partner) -> dict:
#     return {
#         "id" : str(partner["_id"]),
#         "name" : partner["name"],
#         "partner_uuid" : partner["partner_uuid"],
#         "login" : partner["login"],
#         "link" : partner["link"],
#         "logo" : partner["logo"],
#         "issue" : partner["issue"],
#         "is_delete" : partner["is_delete"],
#         "creation_date" : partner["creation_date"]
#     }

# async def list_serial(partners) -> list:
#     result = []
#     async for partner in partners:
#         result.append(partner)
#     return result