from backend.database import SessionLocal
from backend.services.member_service import MemberService


db = SessionLocal()
service = MemberService()

print("=== 회원가입 테스트 ===")

member = service.signup(
    db,
    username="testuser",
    password="1234",
    nickname="테스터"
)

print("가입 결과:", member.id, member.username)


print("\n=== 로그인 테스트 ===")

login_member = service.login