import bcrypt
from datetime import datetime

from backend.repositories.member_repository import MemberRepository
from backend.models.member import Member
from backend.exceptions.error_code import (
    ErrorCode
)

from backend.exceptions.custom_exception import (
    CustomException
)

class MemberService:

    def __init__(self):
        self.member_repository = MemberRepository()

    # -------------------------
    # 회원가입
    # -------------------------
    def signup(self, db, username, password, nickname):

        # 1. 중복 체크
        existing = self.member_repository.find_by_username(db, username)

        if existing:
            raise CustomException(
                ErrorCode.DUPLICATE_USERNAME
            )
        # 2. 비밀번호 암호화
        hashed_pw = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        # 3. Member 생성
        member = Member(
            username=username,
            password=hashed_pw.decode("utf-8"),
            nickname=nickname,
            role="USER",
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # 4. 저장
        return self.member_repository.save(db, member)

    # -------------------------
    # 로그인
    # -------------------------
    def login(self, db, username, password):

        member = self.member_repository.find_by_username(db, username)

        if not member:
            raise CustomException(
                ErrorCode.MEMBER_NOT_FOUND
            )

        if member.is_deleted:
            raise Exception("탈퇴한 사용자입니다.")

        # 비밀번호 검증
        if not bcrypt.checkpw(
            password.encode("utf-8"),
            member.password.encode("utf-8")
        ):
            raise CustomException(
                ErrorCode.INVALID_PASSWORD
            )

        return member

    # -------------------------
    # 회원 조회 (관리자용)
    # -------------------------
    def get_all_members(self, db):

        return self.member_repository.find_all(db)

    # -------------------------
    # 회원 단건 조회
    # -------------------------
    def get_member(self, db, member_id):

        member = self.member_repository.find_by_id(db, member_id)

        if not member:
            raise Exception("사용자를 찾을 수 없습니다.")

        return member

    # -------------------------
    # 회원 삭제 (soft delete)
    # -------------------------
    def delete_member(self, db, member_id):

        member = self.member_repository.find_by_id(db, member_id)

        if not member:
            raise Exception("사용자를 찾을 수 없습니다.")

        member.is_deleted = True
        member.deleted_at = datetime.now()

        return self.member_repository.save(db, member)
    