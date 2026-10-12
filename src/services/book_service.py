import uuid
from typing import Annotated

from fastapi import Depends

from src.models.auditable import utc_now
from src.models.book import BookCreate, BookORM, BookUpdate
from src.repositories.book_repository import BookRepository, BookRepositoryDep


class BookService:
    """Сервіс для роботи з книгами у PostgreSQL з підтримкою аудиту."""

    def __init__(self, repository: BookRepository) -> None:
        self._repository = repository

    async def get_all(self) -> list[BookORM]:
        """Отримати всі книги з БД."""
        return await self._repository.find_all()

    async def get_by_id(self, book_id: str) -> BookORM | None:
        """Отримати книгу за її ID."""
        return await self._repository.find_by_id(book_id)

    async def create(self, data: BookCreate, auditor: str = "Admin") -> BookORM:
        """Створити нову книгу в БД із заповненням метаданих аудиту."""
        now = utc_now()
        book = BookORM(
            id=str(uuid.uuid4()),
            title=data.title,
            author=data.author,
            description=data.description,
            price=data.price,
            published_year=data.published_year,
            created_date=now,
            created_by=auditor,
            last_modified_date=now,
            last_modified_by=auditor,
            version=1,
        )
        return await self._repository.save(book)

    async def update(
        self,
        book_id: str,
        data: BookUpdate,
        auditor: str = "Admin",
    ) -> BookORM | None:
        """Оновити існуючу книгу в БД та інкрементувати версію аудиту."""
        existing = await self._repository.find_by_id(book_id)
        if existing is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field_name, value in update_data.items():
            setattr(existing, field_name, value)

        existing.last_modified_date = utc_now()
        existing.last_modified_by = auditor
        existing.version += 1

        return await self._repository.save(existing)

    async def delete(self, book_id: str) -> bool:
        """Видалити книгу за її ID."""
        return await self._repository.delete_by_id(book_id)


def get_book_service(repository: BookRepositoryDep) -> BookService:
    return BookService(repository)


BookServiceDep = Annotated[BookService, Depends(get_book_service)]
