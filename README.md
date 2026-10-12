# Web Security Labs

Бекенд на FastAPI для лабораторних робіт з курсу безпеки веб-систем.

## Запуск

### Через Docker

```bash
docker compose up -d --build
```

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Зупинка контейнерів:
```bash
docker compose down
```

### Локально

```bash
uv sync
uv run uvicorn src.main:app --reload
```

## Тести та перевірка коду

```bash
uv run pytest
uv run ruff check .
uv run mypy src tests
```

## Лабораторна робота 1

CRUD API з In-Memory сховищем для сутності `Book`:
- `GET /api/v1/books` — список усіх книг
- `GET /api/v1/books/{id}` — отримання книги за ID
- `POST /api/v1/books` — створення книги
- `PUT /api/v1/books/{id}` — оновлення книги
- `DELETE /api/v1/books/{id}` — видалення книги

## Лабораторна робота 3

Додано автентифікацію та авторизацію на базі `fastapi.security` (`HTTPBasic` та `HTTPBearer` / JWT):
- `POST /api/v1/auth/login` — вхід у систему (`admin` / `admin`) та отримання JWT-токена (`200 OK`)
- Усі `GET`-ендпоінти (`GET /`, `GET /health`, `GET /api/v1/books`, `GET /api/v1/books/{id}`) відкриті (`200 OK`)
- Усі НЕ-`GET` ендпоінти (`POST /api/v1/books`, `PUT /api/v1/books/{id}`, `DELETE /api/v1/books/{id}`) захищені залежністю `CurrentUserDep` і без авторизації повертають `401 Unauthorized`
- HTTP-тести:
  - Автотести `pytest`: `tests/test_http_auth.py`
  - HTTP-файл для IDE: `tests/http/basic-authorization.http`


