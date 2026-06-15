from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.schemas.board import (
    BoardCreateRequest,
    BoardUpdateRequest,
    BoardResponse
)
from backend.services.board_service import BoardService

router = APIRouter(
    prefix="/boards",
    tags=["Boards"]
)

service = BoardService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[BoardResponse])
def get_boards(
        db: Session = Depends(get_db)
):
    return service.get_all_boards(db)


@router.get("/{board_id}", response_model=BoardResponse)
def get_board(
        board_id: int,
        db: Session = Depends(get_db)
):
    try:
        return service.get_board(db, board_id)

    except Exception as e:
        raise HTTPException(404, str(e))


@router.post("", response_model=BoardResponse)
def create_board(
        member_id: int,
        request: BoardCreateRequest,
        db: Session = Depends(get_db)
):
    try:
        return service.create_board(
            db,
            member_id,
            request.title,
            request.content
        )

    except Exception as e:
        raise HTTPException(400, str(e))


@router.put("/{board_id}", response_model=BoardResponse)
def update_board(
        board_id: int,
        request: BoardUpdateRequest,
        db: Session = Depends(get_db)
):
    try:
        return service.update_board(
            db,
            board_id,
            request.title,
            request.content
        )

    except Exception as e:
        raise HTTPException(400, str(e))


@router.delete("/{board_id}")
def delete_board(
        board_id: int,
        db: Session = Depends(get_db)
):
    try:
        service.delete_board(db, board_id)

        return {"message": "게시글 삭제 완료"}

    except Exception as e:
        raise HTTPException(404, str(e))