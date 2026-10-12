from typing import Annotated

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import DbSessionDep
from src.models.book import BookORM


class BookRepository:
    """Репозиторій для роботи з сутністю Book у PostgreSQL (аналог ItemRepository)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self) -> list[BookORM]:
        """Отримати всі книги з БД."""
        stmt = select(BookORM).order_by(BookORM.created_date.asc(), BookORM.id.asc())
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def find_by_id(self, book_id: str) -> BookORM | None:
        """Знайти книгу за її ID."""
        return await self._session.get(BookORM, book_id)

    async def save(self, book: BookORM) -> BookORM:
        """Зберегти нову або оновлену книгу в БД."""
        self._session.add(book)
        await self._session.commit()
        await self._session.refresh(book)
        return book

    async def save_all(self, books: list[BookORM]) -> list[BookORM]:
        """Зберегти список книг у БД."""
        self._session.add_all(books)
        await self._session.commit()
        for book in books:
            await self._session.refresh(book)
        return books

    async def delete_by_id(self, book_id: str) -> bool:
        """Видалити книгу за її ID."""
        existing = await self.find_by_id(book_id)
        if existing is None:
            return False
        await self._session.delete(existing)
        await self._session.commit()
        return True

    async def delete_all(self) -> None:
        """Очистити таблицю книг."""
        await self._session.execute(delete(BookORM))
        await self._session.commit()


def get_book_repository(session: DbSessionDep) -> BookRepository:
    return BookRepository(session)


BookRepositoryDep = Annotated[BookRepository, Depends(get_book_repository)]
