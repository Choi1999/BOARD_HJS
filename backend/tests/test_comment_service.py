from backend.database import SessionLocal
from backend.services.comment_service import CommentService

db = SessionLocal()
service = CommentService()

print("\n==== COMMENT SERVICE TEST ====\n")

# -------------------------
# 1. 댓글 생성
# -------------------------
comment = service.create_comment(
    db,
    board_id=1,
    member_id=1,
    content="댓글 테스트"
)

print("댓글 생성:", comment.id)

# -------------------------
# 2. 게시글 기준 조회
# -------------------------
comments = service.get_comments_by_board(db, 1)

print("댓글 수:", len(comments))

# -------------------------
# 3. 삭제
# -------------------------
service.delete_comment(db, comment.id)

print("댓글 삭제 완료")

db.close()