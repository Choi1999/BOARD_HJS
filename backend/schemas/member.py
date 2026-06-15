from pydantic import BaseModel
from datetime import datetime


class MemberSignupRequest(BaseModel):
    username: str
    password: str
    nickname: str


class MemberLoginRequest(BaseModel):
    username: str
    password: str


class MemberResponse(BaseModel):
    id: int
    username: str
    nickname: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True