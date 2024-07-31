import uuid as uuid_pkg
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class UserRole(Enum):
    SUPER_ADMIN = "super_admin"
    ORG_HEAD = "org_head"
    PLAYER = "player"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, onupdate=lambda: datetime.now(timezone.utc))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, username={self.username}, role={self.role}, organization_id={self.organization_id})>"

