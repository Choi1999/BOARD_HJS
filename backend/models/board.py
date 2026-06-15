from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from backend.database import Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    member_id = Column(
        BigInteger,
        ForeignKey("members.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    view_count = Column(
        Integer,
        nullable=False,
        default=0
    )

    is_deleted = Column(
        Boolean,
        nullable=False,
        default=False
    )

    deleted_at = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    member = relationship(
        "Member",
        backref="boards"
    )