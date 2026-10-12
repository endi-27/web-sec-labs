from httpx import AsyncClient


async def test_01_get_all_books(authorized_client: AsyncClient) -> None:
    """1. GET All books — отримання списку всіх книг з PostgreSQL із полями аудиту (200 OK)."""
    response = await authorized_client.get("/api/v1/books")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 3
    first = books[0]
    assert "created_date" in first
    assert first["created_by"] == "Admin"
    assert "last_modified_date" in first
    assert first["last_modified_by"] == "Admin"
    assert first["version"] == 1


async def test_02_get_one_book(authorized_client: AsyncClient) -> None:
    """2. GET one book — отримання однієї книги за ID=2 з полями аудиту (200 OK)."""
    response = await authorized_client.get("/api/v1/books/2")
    assert response.status_code == 200
    book = response.json()
    assert book["id"] == "2"
    assert book["created_by"] == "Admin"
    assert book["version"] == 1


async def test_03_create_one_book(authorized_client: AsyncClient) -> None:
    """3. CREATE one book — створення нової книги в PostgreSQL з аудитом (200 OK)."""
    response = await authorized_client.post(
        "/api/v1/books",
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
    assert created["title"] == "Zero Trust Networks"
    assert created["created_by"] == "admin"
    assert created["last_modified_by"] == "admin"
    assert created["version"] == 1
    assert "created_date" in created
    assert "last_modified_date" in created


async def test_04_update_one_book(authorized_client: AsyncClient) -> None:
    """4. Update one book — оновлення книги змінює last_modified_by та інкрементує version (200 OK)."""
    response = await authorized_client.put(
        "/api/v1/books/1",
        json={
            "title": "Web Application Security (Updated)",
            "description": "Updated description with audit metadata",
            "price": 34.99,
        },
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == "1"
    assert updated["title"] == "Web Application Security (Updated)"
    assert updated["created_by"] == "Admin"
    assert updated["last_modified_by"] == "admin"
    assert updated["version"] == 2


async def test_05_delete_one_book(authorized_client: AsyncClient) -> None:
    """5. DELETE one book — видалення книги з PostgreSQL проходить успішно (200 OK)."""
    delete_res = await authorized_client.delete("/api/v1/books/1")
    assert delete_res.status_code == 200

    get_res = await authorized_client.get("/api/v1/books/1")
    assert get_res.status_code == 404
