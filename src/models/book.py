import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.auditable import AuditableMixin, AuditableSchema


class BookORM(AuditableMixin, Base):
    """ORM-модель книги в PostgreSQL з полями аудиту (аналог Item extends Auditable)."""

    __tablename__ = "books"

    id: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)


class BookBase(BaseModel):
    """Базова схема книги з основними полями."""

    title: Annotated[
        str,
        Field(
            min_length=1,
            max_length=200,
            description="Назва книги",
            examples=["Web Application Security"],
        ),
    ]
    author: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="Автор книги",
            examples=["Andrew Hoffman"],
        ),
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            max_length=1000,
            description="Короткий опис / анотація",
            examples=["Exploitation and Countermeasures for Modern Web Applications"],
        ),
    ] = None
    price: Annotated[
        float,
        Field(
            ge=0.0,
            description="Ціна книги",
            examples=[39.99],
        ),
    ]
    published_year: Annotated[
        int | None,
        Field(
            default=None,
            ge=1000,
            le=2100,
            description="Рік видання",
            examples=[2020],
        ),
    ] = None


class BookCreate(BookBase):
    """Схема для створення нової книги."""

    pass


class BookUpdate(BaseModel):
    """Схема для часткового або повного оновлення книги."""

    title: Annotated[
        str | None,
        Field(
            default=None,
            min_length=1,
            max_length=200,
            description="Нова назва книги",
        ),
    ] = None
    author: Annotated[
        str | None,
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="Новий автор книги",
        ),
    ] = None
    description: Annotated[
        str | None,
        Field(
            default=None,
            max_length=1000,
            description="Новий опис",
        ),
    ] = None
    price: Annotated[
        float | None,
        Field(
            default=None,
            ge=0.0,
            description="Нова ціна",
        ),
    ] = None
    published_year: Annotated[
        int | None,
        Field(
            default=None,
            ge=1000,
            le=2100,
            description="Новий рік видання",
        ),
    ] = None


class Book(BookBase, AuditableSchema):
    """Внутрішня модель сутності книги з полями аудиту."""

    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="Унікальний ідентифікатор книги",
        ),
    ]


class BookResponse(Book):
    """Схема відповіді для API."""

    model_config = ConfigDict(from_attributes=True)
