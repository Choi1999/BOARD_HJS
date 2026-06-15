from datetime import datetime

from backend.repositories.comment_repository import CommentRepository
from backend.models.comment import Comment
from backend.exceptions.error_code import (
    ErrorCode
)

from backend.exceptions.custom_exception import (
    CustomException
)

class CommentService:

    def __init__(self):
        self.comment_repository = CommentRepository()

    def create_comment(self, db, board_id, member_id, content):

        comment = Comment(
            board_id=board_id,
            member_id=member_id,
            content=content,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.comment_repository.save(db, comment)

    def get_comments_by_board(self, db, board_id):
        return self.comment_repository.find_by_board_id(db, board_id)

    def delete_comment(self, db, comment_id):

        comment = self.comment_repository.find_by_id(db, comment_id)

        if not comment:
            raise CustomException(
                ErrorCode.COMMENT_NOT_FOUND
            )   
        return self.comment_repository.delete(db, comment)