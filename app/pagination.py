from __future__ import annotations


from typing import Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel
from starlette.requests import Request

from fastapi_paginate.bases import AbstractPage, AbstractParams, RawParams

T = TypeVar("T")

class Params(BaseModel, AbstractParams):
    page: int = Query(1, ge=1, description="Page number")
    pageSize: int = Query(10, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.pageSize,
            offset=self.pageSize * (self.page - 1),
        )


class Page(AbstractPage[T], Generic[T]):
    total: Optional[int] = 0
    data : Sequence[T]# type: ignore
    
    __params_type__ = Params

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: AbstractParams, request: Request) -> Page[T]:
        return cls(
            total=total,
            data=items
        )


__all__ = [
    "Params",
    "Page",
]
