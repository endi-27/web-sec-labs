from httpx import AsyncClient


async def _get_token(client: AsyncClient, username: str, password: str) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    token: str = response.json()["access_token"]
    return token


async def test_01_login_admin_jwt(client: AsyncClient) -> None:
    """1. POST /api/v1/auth/login під admin — 200 OK та валідний JWT токен."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "ADMIN"
    assert data["authorities"] == ["ADMIN"]
    assert "access_token" in data


async def test_02_login_user_jwt(client: AsyncClient) -> None:
    """2. POST /api/v1/auth/login під user — 200 OK та валідний JWT токен."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "user", "password": "user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "USER"
    assert data["authorities"] == ["USER"]
    assert "access_token" in data


async def test_03_hello_admin_with_admin_jwt_succeeds(client: AsyncClient) -> None:
    """3. GET /api/v1/hello/admin з Bearer JWT токеном admin — 200 OK."""
    token = await _get_token(client, "admin", "admin")
    response = await client.get(
        "/api/v1/hello/admin",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello Admin!"
    assert data["role"] == "ADMIN"


async def test_04_hello_admin_with_user_jwt_forbidden(client: AsyncClient) -> None:
    """4. GET /api/v1/hello/admin з Bearer JWT токеном user — 403 Forbidden."""
    token = await _get_token(client, "user", "user")
    response = await client.get(
        "/api/v1/hello/admin",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
    assert "не входить до дозволених" in response.json()["detail"]


async def test_05_hello_user_with_user_jwt_succeeds(client: AsyncClient) -> None:
    """5. GET /api/v1/hello/user з Bearer JWT токеном user — 200 OK."""
    token = await _get_token(client, "user", "user")
    response = await client.get(
        "/api/v1/hello/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello!, user"
    assert data["role"] == "USER"


async def test_06_hello_user_with_admin_jwt_forbidden(client: AsyncClient) -> None:
    """6. GET /api/v1/hello/user з Bearer JWT токеном admin — 403 Forbidden."""
    token = await _get_token(client, "admin", "admin")
    response = await client.get(
        "/api/v1/hello/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
    assert "не входить до дозволених" in response.json()["detail"]


async def test_07_hello_man_with_user_jwt_succeeds(client: AsyncClient) -> None:
    """7. GET /api/v1/hello/man з Bearer JWT токеном user — 200 OK."""
    token = await _get_token(client, "user", "user")
    response = await client.get(
        "/api/v1/hello/man",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, man!"


async def test_08_hello_man_with_admin_jwt_succeeds(client: AsyncClient) -> None:
    """8. GET /api/v1/hello/man з Bearer JWT токеном admin — 200 OK."""
    token = await _get_token(client, "admin", "admin")
    response = await client.get(
        "/api/v1/hello/man",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Hello, man!"


async def test_09_hello_unknown_with_user_jwt_succeeds(client: AsyncClient) -> None:
    """9. GET /api/v1/hello/unknown з Bearer JWT токеном user — 200 OK."""
    token = await _get_token(client, "user", "user")
    response = await client.get(
        "/api/v1/hello/unknown",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello Unknown!"
    assert data["role"] == "USER"


async def test_10_hello_admin_without_jwt_unauthorized(client: AsyncClient) -> None:
    """10. GET /api/v1/hello/admin без токена (анонімно) — 401 Unauthorized."""
    response = await client.get("/api/v1/hello/admin")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers
