from backend.database import SessionLocal
from backend.services.board_service import BoardService

db = SessionLocal()
service = BoardService()

print("\n==== BOARD SERVICE TEST ====\n")

# -------------------------
# 1. 게시글 생성
# -------------------------
board = service.create_board(
    db,
    member_id=1,
    title="첫 게시글",
    content="내용입니다"
)

print("게시글 생성:", board.id, board.title)

# -------------------------
# 2. 전체 조회
# -------------------------
boards = service.get_all_boards(db)

print("전체 게시글:", len(boards))

# -------------------------
# 3. 단건 조회
# -------------------------
one = service.get_board(db, board.id)

print("단건 조회:", one.title)

# -------------------------
# 4. 수정
# -------------------------
updated = service.update_board(
    db,
    board.id,
    "수정된 제목",
    "수정된 내용"
)

print("수정 완료:", updated.title)

# -------------------------
# 5. 삭제
# -------------------------
service.delete_board(db, board.id)

print("삭제 완료")

db.close()