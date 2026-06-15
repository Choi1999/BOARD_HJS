from sqlalchemy.orm import Session

from backend.models.comment import Comment


class CommentRepository:

    def find_by_board_id(
            self,
            db: Session,
            board_id: int
    ):

        return (
            db.query(Comment)
            .filter(
                Comment.board_id == board_id,
                Comment.is_deleted == False
            )
            .all()
        )
    def find_by_id(
            self,
            db: Session,
            comment_id: int
    ):

        return (
            db.query(Comment)
            .filter(
                Comment.id == comment_id,
                Comment.is_deleted == False
            )
            .first()
        )
    def save(
            self,
            db: Session,
            comment: Comment
    ):

        db.add(comment)

        db.commit()

        db.refresh(comment)

        return comment

    def delete(
            self,
            db: Session,
            comment: Comment
    ):

        comment.is_deleted = True

        db.commit()