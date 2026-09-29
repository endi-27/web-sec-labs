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
