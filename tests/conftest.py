import asyncio
import os
from collections.abc import AsyncIterator

import pytest
from alembic.config import Config
from httpx import ASGITransport, AsyncClient

from alembic import command
from src.main import app


def _run_alembic_reset() -> None:
    """Перезапускає міграції Alembic (downgrade base -> upgrade head) для чистих seed-даних."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(autouse=True)
async def reset_db() -> None:
    """Скидає стан БД (книги та 3 користувачі) через міграції Alembic перед кожним тестом."""
    await asyncio.to_thread(_run_alembic_reset)


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Асинхронний HTTP-клієнт (підтримує реальні запити до Docker-контейнера через TEST_BASE_URL)."""
    base_url = os.getenv("TEST_BASE_URL")
    if base_url:
        async with AsyncClient(base_url=base_url) as ac:
            yield ac
    else:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac
