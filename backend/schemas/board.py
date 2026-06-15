from pydantic import BaseModel
from datetime import datetime


class BoardCreateRequest(BaseModel):
    title: str
    content: str


class BoardUpdateRequest(BaseModel):
    title: str
    content: str


class BoardResponse(BaseModel):
    id: int
    member_id: int
    title: str
    content: str
    view_count: int
    created_at: datetime

    class Config:
        from_attributes = True