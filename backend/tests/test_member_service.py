from backend.database import SessionLocal
from backend.services.member_service import MemberService

db = SessionLocal()
service = MemberService()

print("\n==== MEMBER SERVICE TEST ====\n")

# -------------------------
# 1. 회원가입 테스트
# -------------------------
member = service.signup(
    db,
    username="user1",
    password="1234",
    nickname="유저1"
)

print("회원가입:", member.id, member.username)

# -------------------------
# 2. 로그인 테스트
# -------------------------
login_member = service.login(
    db,
    username="user1",
    password="1234"
)

print("로그인 성공:", login_member.username)

# -------------------------
# 3. 전체 조회
# -------------------------
all_members = service.get_all_members(db)

print("전체 회원 수:", len(all_members))

db.close()