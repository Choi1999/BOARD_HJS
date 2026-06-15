from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.schemas.comment import (
    CommentCreateRequest,
    CommentResponse
)
from backend.services.comment_service import CommentService

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

service = CommentService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=CommentResponse)
def create_comment(
        member_id: int,
        request: CommentCreateRequest,
        db: Session = Depends(get_db)
):
    try:
        return service.create_comment(
            db,
            request.board_id,
            member_id,
            request.content
        )

    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/board/{board_id}",
            response_model=list[CommentResponse])
def get_comments(
        board_id: int,
        db: Session = Depends(get_db)
):
    return service.get_comments_by_board(
        db,
        board_id
    )


@router.delete("/{comment_id}")
def delete_comment(
        comment_id: int,
        db: Session = Depends(get_db)
):
    try:
        service.delete_comment(
            db,
            comment_id
        )

        return {
            "message": "댓글 삭제 완료"
        }

    except Exception as e:
        raise HTTPException(404, str(e))