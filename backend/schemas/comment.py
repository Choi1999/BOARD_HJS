from pydantic import BaseModel
from datetime import datetime


class CommentCreateRequest(BaseModel):
    board_id: int
    content: str


class CommentResponse(BaseModel):
    id: int
    board_id: int
    member_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True