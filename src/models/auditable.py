from datetime import UTC, datetime
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


def utc_now() -> datetime:
    """Повертає поточний час в UTC."""
    return datetime.now(UTC)


class AuditableMixin:
    """Mixin-клас аудиту для SQLAlchemy моделей (аналог Auditable у Spring Data)."""

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    created_by: Mapped[str] = mapped_column(
        String(100),
        default="Admin",
        nullable=False,
    )
    last_modified_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
    last_modified_by: Mapped[str] = mapped_column(
        String(100),
        default="Admin",
        nullable=False,
    )
    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )


class AuditableSchema(BaseModel):
    """Pydantic-схема полів аудиту для відповідей API."""

    created_date: Annotated[
        datetime,
        Field(description="Дата та час створення запису"),
    ]
    created_by: Annotated[
        str,
        Field(description="Користувач, який створив запис", examples=["admin"]),
    ]
    last_modified_date: Annotated[
        datetime,
        Field(description="Дата та час останньої модифікації запису"),
    ]
    last_modified_by: Annotated[
        str,
        Field(description="Користувач, який останнім змінив запис", examples=["admin"]),
    ]
    version: Annotated[
        int,
        Field(ge=1, description="Версія запису (інкрементується при оновленні)", examples=[1]),
    ]
