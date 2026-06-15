from datetime import datetime

from backend.repositories.board_repository import BoardRepository
from backend.models.board import Board
from backend.exceptions.error_code import (
    ErrorCode
)

from backend.exceptions.custom_exception import (
    CustomException
)

class BoardService:

    def __init__(self):
        self.board_repository = BoardRepository()

    def create_board(self, db, member_id, title, content):

        board = Board(
            member_id=member_id,
            title=title,
            content=content,
            view_count=0,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        return self.board_repository.save(db, board)

    def get_all_boards(self, db):
        return self.board_repository.find_all(db)

    def get_board(self, db, board_id):

        board = self.board_repository.find_by_id(db, board_id)

        if not board:
            raise Exception("게시글이 존재하지 않습니다.")

        return board

    def update_board(self, db, board_id, title, content):

        board = self.board_repository.find_by_id(db, board_id)

        if not board:
            raise CustomException(
                ErrorCode.BOARD_NOT_FOUND
            )
        board.title = title
        board.content = content
        board.updated_at = datetime.now()

        return self.board_repository.save(db, board)

    def delete_board(self, db, board_id):

        board = self.board_repository.find_by_id(db, board_id)

        if not board:
            raise Exception("게시글이 존재하지 않습니다.")

        return self.board_repository.delete(db, board)