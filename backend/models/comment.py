from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from backend.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    board_id = Column(
        BigInteger,
        ForeignKey("boards.id"),
        nullable=False
    )

    member_id = Column(
        BigInteger,
        ForeignKey("members.id"),
        nullable=False
    )

    content = Column(
        String(1000),
        nullable=False
    )

    is_deleted = Column(
        Boolean,
        nullable=False,
        default=False
    )

    deleted_at = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    board = relationship(
        "Board",
        backref="comments"
    )

    member = relationship(
        "Member",
        backref="comments"
    )