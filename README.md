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

## Лабораторна робота 4

Інтеграція з PostgreSQL, патерн Repository, аудит записів (`AuditableMixin`) та повноцінний авторизований CRUD:
- **База даних та Repository**: перехід з in-memory `dict` на асинхронну PostgreSQL (`SQLAlchemy 2.0` + `asyncpg`) через `BookRepository` (`src/repositories/book_repository.py`).
- **Аудит (`AuditableMixin`)**: додано метадані аудиту до моделі `BookORM` та схеми `BookResponse` (`created_date`, `created_by`, `last_modified_date`, `last_modified_by`, `version`).
- **Авторизація всіх ендпоінтів `/api/v1/books`**: усі операції (`GET`, `POST`, `PUT`, `DELETE`) захищені та успішно виконуються при передачі Basic Auth або Bearer JWT токена.

## Лабораторна робота 5

Багатокористувацька модель (Multi-User) та рольовий контроль доступу (RBAC):
- **Таблиця `users` та ролі `UserRole(StrEnum)`**: створено сутність `UserORM` (`src/models/user.py`), `UserRepository` (`src/repositories/user_repository.py`) та міграцію Alembic `0002_create_users_and_seed.py`, яка сідує 3 користувачів з `bcrypt`-паролями:
  - `admin` / `admin` (`ADMIN`)
  - `user` / `user` (`USER`)
  - `superadmin` / `superadmin` (`SUPERADMIN`)
- **Динамічні залежності авторизації (`src/controllers/dependencies.py`)**: винесено `get_current_user` та фабрику залежностей `require_roles(*allowed_roles: UserRole)` для гнучкої перевірки ролей на рівні ендпоінтів.
- **20 HTTP-тестів за ролями**:
  - Файл для VS Code REST Client: `tests/http/multi-user-basic.http`
  - Автотести `pytest`: `tests/test_http_auth.py`

## Лабораторна робота 6

Контроль доступу на рівні методів (Method-Level Security) та анотації доступу:
- **Архітектурні особливості FastAPI vs Spring Security**: на відміну від Spring Security (де на попередніх кроках налаштовувався глобальний фільтр `SecurityFilterChain` з URL-мапінгом ролей), у FastAPI стандартним та ідіоматичним підходом є оголошення вимог безпеки безпосередньо над обробниками маршрутів за допомогою Dependency Injection (`typing.Annotated[UserResponse, Depends(require_roles(...))]`).
- **Захист ендпоінтів**: кожен метод контролерів (`hello_controller.py`, `book_controller.py`) має власну декларативну анотацію дозволених ролей (RBAC).
- **Хешування паролів**: підтверджено використання алгоритму `bcrypt` для збереження паролів у БД замість відкритого тексту.





