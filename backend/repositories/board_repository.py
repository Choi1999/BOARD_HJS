from sqlalchemy.orm import Session

from backend.models.board import Board


class BoardRepository:

    def find_all(
            self,
            db: Session
    ):

        return (
            db.query(Board)
            .filter(
                Board.is_deleted == False
            )
            .order_by(Board.created_at.desc())
            .all()
        )

    def find_by_id(
            self,
            db: Session,
            board_id: int
    ):

        return (
            db.query(Board)
            .filter(
                Board.id == board_id,
                Board.is_deleted == False
            )
            .first()
        )

    def save(
            self,
            db: Session,
            board: Board
    ):

        db.add(board)

        db.commit()

        db.refresh(board)

        return board

    def delete(
            self,
            db: Session,
            board: Board
    ):

        board.is_deleted = True

        db.commit()