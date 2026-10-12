from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import DbSessionDep
from src.models.user import UserORM


class UserRepository:
    """Репозиторій для роботи з сутністю User у PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_username(self, username: str) -> UserORM | None:
        """Знайти користувача за його логіном (username)."""
        stmt = select(UserORM).where(UserORM.username == username)
        return await self._session.scalar(stmt)

    async def find_by_id(self, user_id: str) -> UserORM | None:
        """Знайти користувача за його ID."""
        return await self._session.get(UserORM, user_id)

    async def find_all(self) -> list[UserORM]:
        """Отримати всіх користувачів з БД."""
        stmt = select(UserORM).order_by(UserORM.created_date.asc(), UserORM.id.asc())
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def save(self, user: UserORM) -> UserORM:
        """Зберегти нового або оновленого користувача в БД."""
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user


def get_user_repository(session: DbSessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
