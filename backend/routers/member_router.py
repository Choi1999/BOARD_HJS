from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.schemas.member import (
    MemberSignupRequest,
    MemberLoginRequest,
    MemberResponse
)
from backend.services.member_service import MemberService

router = APIRouter(
    prefix="/members",
    tags=["Members"]
)

service = MemberService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=MemberResponse)
def signup(
        request: MemberSignupRequest,
        db: Session = Depends(get_db)
):
    try:
        return service.signup(
            db,
            request.username,
            request.password,
            request.nickname
        )
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/login", response_model=MemberResponse)
def login(
        request: MemberLoginRequest,
        db: Session = Depends(get_db)
):
    try:
        return service.login(
            db,
            request.username,
            request.password
        )
    except Exception as e:
        raise HTTPException(401, str(e))


@router.get("", response_model=list[MemberResponse])
def get_members(
        db: Session = Depends(get_db)
):
    return service.get_all_members(db)