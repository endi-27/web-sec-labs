from httpx import AsyncClient


async def test_01_hello_admin_as_admin_succeeds(client: AsyncClient) -> None:
    """1. GET /api/v1/hello/admin під admin (ADMIN) — 200 OK."""
    response = await client.get("/api/v1/hello/admin", auth=("admin", "admin"))
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello Admin!"
    assert data["role"] == "ADMIN"


async def test_02_hello_admin_as_user_forbidden(client: AsyncClient) -> None:
    """2. GET /api/v1/hello/admin під user (USER) — 403 Forbidden."""
    response = await client.get("/api/v1/hello/admin", auth=("user", "user"))
    assert response.status_code == 403


async def test_03_hello_admin_as_superadmin_forbidden(client: AsyncClient) -> None:
    """3. GET /api/v1/hello/admin під superadmin (SUPERADMIN) — 403 Forbidden."""
    response = await client.get("/api/v1/hello/admin", auth=("superadmin", "superadmin"))
    assert response.status_code == 403


async def test_04_hello_user_as_user_succeeds(client: AsyncClient) -> None:
    """4. GET /api/v1/hello/user під user (USER) — 200 OK."""
    response = await client.get("/api/v1/hello/user", auth=("user", "user"))
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello!, user"
    assert data["role"] == "USER"


async def test_05_hello_user_as_admin_forbidden(client: AsyncClient) -> None:
    """5. GET /api/v1/hello/user під admin (ADMIN) — 403 Forbidden."""
    response = await client.get("/api/v1/hello/user", auth=("admin", "admin"))
    assert response.status_code == 403


async def test_06_hello_man_as_user_succeeds(client: AsyncClient) -> None:
    """6. GET /api/v1/hello/man під user (дозволено USER, ADMIN) — 200 OK."""
    response = await client.get("/api/v1/hello/man", auth=("user", "user"))
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, man!"


async def test_07_hello_man_as_admin_succeeds(client: AsyncClient) -> None:
    """7. GET /api/v1/hello/man під admin (дозволено USER, ADMIN) — 200 OK."""
    response = await client.get("/api/v1/hello/man", auth=("admin", "admin"))
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, man!"


async def test_08_hello_man_as_superadmin_forbidden(client: AsyncClient) -> None:
    """8. GET /api/v1/hello/man під superadmin (SUPERADMIN) — 403 Forbidden."""
    response = await client.get("/api/v1/hello/man", auth=("superadmin", "superadmin"))
    assert response.status_code == 403


async def test_09_hello_superadmin_as_superadmin_succeeds(client: AsyncClient) -> None:
    """9. GET /api/v1/hello/superadmin під superadmin (SUPERADMIN) — 200 OK."""
    response = await client.get("/api/v1/hello/superadmin", auth=("superadmin", "superadmin"))
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello Superadmin!"
    assert data["role"] == "SUPERADMIN"


async def test_10_hello_superadmin_as_admin_forbidden(client: AsyncClient) -> None:
    """10. GET /api/v1/hello/superadmin під admin (ADMIN) — 403 Forbidden."""
    response = await client.get("/api/v1/hello/superadmin", auth=("admin", "admin"))
    assert response.status_code == 403


async def test_11_hello_unknown_as_user_succeeds(client: AsyncClient) -> None:
    """11. GET /api/v1/hello/unknown під user (будь-яка роль) — 200 OK."""
    response = await client.get("/api/v1/hello/unknown", auth=("user", "user"))
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello Unknown!"
    assert data["role"] == "USER"


async def test_12_hello_unknown_as_superadmin_succeeds(client: AsyncClient) -> None:
    """12. GET /api/v1/hello/unknown під superadmin (будь-яка роль) — 200 OK."""
    response = await client.get("/api/v1/hello/unknown", auth=("superadmin", "superadmin"))
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello Unknown!"
    assert data["role"] == "SUPERADMIN"


async def test_13_get_all_books_as_user_succeeds(client: AsyncClient) -> None:
    """13. GET /api/v1/books під user (USER може читати книги) — 200 OK."""
    response = await client.get("/api/v1/books", auth=("user", "user"))
    assert response.status_code == 200
    assert len(response.json()) == 3


async def test_14_get_book_by_id_as_admin_succeeds(client: AsyncClient) -> None:
    """14. GET /api/v1/books/2 під admin (ADMIN може читати книгу за ID) — 200 OK."""
    response = await client.get("/api/v1/books/2", auth=("admin", "admin"))
    assert response.status_code == 200
    assert response.json()["id"] == "2"


async def test_15_create_book_as_user_forbidden(client: AsyncClient) -> None:
    """15. POST /api/v1/books під user (USER не може створювати книги) — 403 Forbidden."""
    response = await client.post(
        "/api/v1/books",
        auth=("user", "user"),
        json={
            "title": "Forbidden Book by User",
            "author": "Regular User",
            "price": 25.00,
        },
    )
    assert response.status_code == 403


async def test_16_create_book_as_admin_succeeds(client: AsyncClient) -> None:
    """16. POST /api/v1/books під admin (ADMIN може створювати книги) — 200 OK."""
    response = await client.post(
        "/api/v1/books",
        auth=("admin", "admin"),
        json={
            "title": "Zero Trust Networks",
            "author": "Evan Gilman, Doug Barth",
            "description": "Building Secure Systems in Untrusted Networks",
            "price": 45.00,
            "published_year": 2017,
        },
    )
    assert response.status_code == 200
    created = response.json()
    assert created["created_by"] == "admin"
    assert created["version"] == 1


async def test_17_update_book_as_user_forbidden(client: AsyncClient) -> None:
    """17. PUT /api/v1/books/2 під user (USER не може оновлювати книги) — 403 Forbidden."""
    response = await client.put(
        "/api/v1/books/2",
        auth=("user", "user"),
        json={"title": "Forbidden Update by User", "price": 10.00},
    )
    assert response.status_code == 403


async def test_18_update_book_as_superadmin_succeeds(client: AsyncClient) -> None:
    """18. PUT /api/v1/books/2 під superadmin (SUPERADMIN оновлює книгу) — 200 OK."""
    response = await client.put(
        "/api/v1/books/2",
        auth=("superadmin", "superadmin"),
        json={
            "title": "The Web Application Hacker's Handbook (2nd Edition)",
            "price": 54.99,
        },
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["last_modified_by"] == "superadmin"
    assert updated["version"] == 2


async def test_19_delete_book_as_admin_forbidden(client: AsyncClient) -> None:
    """19. DELETE /api/v1/books/1 під admin (ADMIN не може видаляти книги) — 403 Forbidden."""
    response = await client.delete("/api/v1/books/1", auth=("admin", "admin"))
    assert response.status_code == 403


async def test_20_delete_book_as_superadmin_succeeds(client: AsyncClient) -> None:
    """20. DELETE /api/v1/books/1 під superadmin (SUPERADMIN видаляє книгу) — 200 OK."""
    response = await client.delete("/api/v1/books/1", auth=("superadmin", "superadmin"))
    assert response.status_code == 200
    assert response.json()["deleted_by"] == "superadmin"
