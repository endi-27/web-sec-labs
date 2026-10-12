import uuid
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.auditable import AuditableMixin, AuditableSchema


class UserRole(StrEnum):
    """Ролі користувачів у системі (RBAC)."""

    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"


class UserORM(AuditableMixin, Base):
    """ORM-модель користувача в PostgreSQL (роль зберігається як String)."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(50),
        default=UserRole.USER.value,
        nullable=False,
    )


class UserCreate(BaseModel):
    """Схема для створення нового користувача."""

    username: Annotated[
        str,
        Field(min_length=1, max_length=100, description="Логін користувача", examples=["admin"]),
    ]
    password: Annotated[
        str,
        Field(min_length=1, max_length=100, description="Пароль користувача", examples=["admin"]),
    ]
    role: Annotated[
        UserRole,
        Field(default=UserRole.USER, description="Роль користувача"),
    ] = UserRole.USER


class UserResponse(AuditableSchema):
    """Схема публічних даних авторизованого користувача."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    role: UserRole
