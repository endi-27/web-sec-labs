import os
from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.main import app
from src.services.auth_service import get_auth_service
from src.services.book_service import get_book_service


@pytest.fixture(autouse=True)
def reset_books() -> None:
    """Скидає in-memory сховище книг перед кожним тестом."""
    get_book_service().seed_data()


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


@pytest.fixture
def admin_credentials() -> tuple[str, str]:
    """Логін і пароль адміністратора за замовчуванням."""
    return settings.security_user_name, settings.security_user_password


@pytest.fixture
def auth_token() -> str:
    """Генерує дійсний JWT Bearer токен для адміністратора."""
    return get_auth_service().create_access_token(settings.security_user_name)


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    """Заголовки авторизації з дійсним Bearer токеном."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
async def authorized_client(auth_headers: dict[str, str]) -> AsyncIterator[AsyncClient]:
    """Асинхронний HTTP-клієнт із попередньо налаштованим Bearer-токеном авторизації."""
    base_url = os.getenv("TEST_BASE_URL")
    if base_url:
        async with AsyncClient(base_url=base_url, headers=auth_headers) as ac:
            yield ac
    else:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver", headers=auth_headers) as ac:
            yield ac
