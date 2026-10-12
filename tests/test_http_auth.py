from httpx import AsyncClient


async def test_01_login_json_succeeds(client: AsyncClient) -> None:
    """1. POST /api/v1/auth/login (JSON) — успішний вхід (200 OK)."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "admin"


async def test_02_login_basic_auth_succeeds(client: AsyncClient) -> None:
    """2. POST /api/v1/auth/login (Basic Auth) — успішний вхід (200 OK)."""
    response = await client.post(
        "/api/v1/auth/login",
        auth=("admin", "admin"),
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_03_get_health_succeeds(client: AsyncClient) -> None:
    """3. GET /health — перевірка стану сервісу проходить без авторизації (200 OK)."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_04_get_all_books_succeeds(client: AsyncClient) -> None:
    """4. GET /api/v1/books — отримання списку книг проходить без авторизації (200 OK)."""
    response = await client.get("/api/v1/books")
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_05_get_book_by_id_succeeds(client: AsyncClient) -> None:
    """5. GET /api/v1/books/1 — отримання книги за ID проходить без авторизації (200 OK)."""
    response = await client.get("/api/v1/books/1")
    assert response.status_code == 200
    assert response.json()["id"] == "1"


async def test_06_post_create_book_without_auth_fails_401(client: AsyncClient) -> None:
    """6. POST /api/v1/books — створення книги без авторизації падає з 401."""
    response = await client.post(
        "/api/v1/books",
        json={
            "title": "Zero Trust Networks",
            "author": "Evan Gilman, Doug Barth",
            "description": "Building Secure Systems in Untrusted Networks",
            "price": 45.00,
            "published_year": 2017,
        },
    )
    assert response.status_code == 401


async def test_07_put_update_book_without_auth_fails_401(client: AsyncClient) -> None:
    """7. PUT /api/v1/books/1 — оновлення книги без авторизації падає з 401."""
    response = await client.put(
        "/api/v1/books/1",
        json={"title": "Web Application Security (Updated)", "price": 34.99},
    )
    assert response.status_code == 401


async def test_08_delete_book_without_auth_fails_401(client: AsyncClient) -> None:
    """8. DELETE /api/v1/books/1 — видалення книги без авторизації падає з 401."""
    response = await client.delete("/api/v1/books/1")
    assert response.status_code == 401


async def test_09_post_create_book_bad_basic_credentials_fails_401(client: AsyncClient) -> None:
    """9. POST /api/v1/books — створення книги з невірними Basic Auth даними падає з 401."""
    response = await client.post(
        "/api/v1/books",
        auth=("admin1", "admin"),
        json={
            "title": "Unauthorized Book",
            "author": "Unknown",
            "price": 19.99,
        },
    )
    assert response.status_code == 401


async def test_10_put_update_book_invalid_bearer_token_fails_401(client: AsyncClient) -> None:
    """10. PUT /api/v1/books/1 — оновлення книги з невалідним JWT токеном падає з 401."""
    response = await client.put(
        "/api/v1/books/1",
        headers={"Authorization": "Bearer invalid.jwt.token"},
        json={"title": "Tampered Book Title", "price": 1.00},
    )
    assert response.status_code == 401
