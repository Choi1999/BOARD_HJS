from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Enum,
    Boolean,
    DateTime
)
from backend.database import Base
import enum


class Role(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class Member(Base):
    __tablename__ = "members"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    username = Column(String(50), nullable=False, unique=True)

    password = Column(String(255), nullable=False)

    nickname = Column(String(50), nullable=False, unique=True)

    role = Column(
        Enum(Role),
        nullable=False,
        default=Role.USER
    )

    is_deleted = Column(
        Boolean,
        nullable=False,
        default=False
    )

    deleted_at = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)