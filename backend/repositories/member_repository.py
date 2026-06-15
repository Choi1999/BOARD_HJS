from sqlalchemy.orm import Session

from backend.models.member import Member


class MemberRepository:

    def find_by_username(
            self,
            db: Session,
            username: str
    ):

        return (
            db.query(Member)
            .filter(
                Member.username == username,
                Member.is_deleted == False
            )
            .first()
        )

    def find_by_id(
            self,
            db: Session,
            member_id: int
    ):

        return (
            db.query(Member)
            .filter(
                Member.id == member_id,
                Member.is_deleted == False
            )
            .first()
        )

    def save(
            self,
            db: Session,
            member: Member
    ):

        db.add(member)
        db.commit()
        db.refresh(member)

        return member

    def find_all(
            self,
            db: Session
    ):

        return (
            db.query(Member)
            .filter(
                Member.is_deleted == False
            )
            .all()
        )