from backend.database import SessionLocal
from backend.repositories.member_repository import MemberRepository


db = SessionLocal()

repo = MemberRepository()

members = repo.find_all(db)

print(members)

db.close()