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

## Лабораторна робота 6

Контроль доступу на рівні методів (Method-Level Security) та анотації доступу:
- **Архітектурні особливості FastAPI vs Spring Security**: на відміну від Spring Security (де у попередніх кроках налаштовувався глобальний фільтр `SecurityFilterChain` з URL-мапінгом ролей), у FastAPI стандартним та ідіоматичним підходом є оголошення вимог безпеки безпосередньо над обробниками маршрутів за допомогою Dependency Injection (`typing.Annotated[UserResponse, Depends(require_roles(...))]`).
- **Захист ендпоінтів**: кожен метод контролерів (`hello_controller.py`, `book_controller.py`) має власну декларативну анотацію дозволених ролей (RBAC).
- **Хешування паролів**: підтверджено використання алгоритму `bcrypt` для збереження паролів у БД замість відкритого тексту.

## Лабораторна робота 7

Автоматизоване тестування безпеки та контролю доступу через `pytest`:
- **Перенесення тестів з REST Client у pytest**: усі 20 сценаріїв із `tests/http/multi-user-basic.http` повністю перенесені у тестовий набір `tests/test_http_auth.py`.
- **Повне покриття статусів безпеки**:
  - `401 Unauthorized`: перевірка неавторизованого доступу анонімних запитів (аналог `whenAnonymThenStatusUnauthorized` з `AccessTests.java` викладача) та запитів із невалідними креденшелами.
  - `200 OK`: перевірка успішного доступу для дозволених ролей (`ADMIN`, `USER`, `SUPERADMIN`) із валідацією тіла відповіді.
  - `403 Forbidden`: перевірка блокування доступу для ролей без достатніх прав.

## Лабораторна робота 8

Автентифікація користувача та генерація JWT токена (JSON Web Token):
- **Генерація JWT (`AuthService.create_access_token`)**: реалізовано створення підписаного токена (HMAC-SHA256) із клеймами:
  - `sub`: ідентифікатор / ім'я користувача (`username`)
  - `role`: роль користувача (`ADMIN`, `USER`, `SUPERADMIN`)
  - `authorities`: список прав/ролей у форматі Spring Security (`["ADMIN"]`, `["USER"]`), що очікується на лекціях
  - `iat`: час видачі токена (Issued At)
  - `exp`: термін дії токена (Expiration Time, 60 хвилин)
- **Ендпоінти автентифікації**:
  - `POST /api/v1/auth/login` — стандартний REST API ендпоінт FastAPI
  - `POST /auth/authenticate` — прямий аліас для повної сумісності з форматом запитів викладача у Spring Boot
  - Підтримка передачі параметрів як `{ "username": "admin", "password": "admin" }`, так і `{ "email": "admin", "password": "admin" }` / `{ "login": "admin", "password": "admin" }`
- **Перевірка у jwt.io**:
  - Отриманий у відповіді токен декодується на веб-сервісі [jwt.io](https://jwt.io)
  - Скріншот розпарсеного JWT із клеймами `sub`, `role`, `authorities`, `iat`, `exp` надсилається у Moodle
- **HTTP-тести**:
  - Pytest автотести: `tests/test_jwt_generation.py`
  - Файл для REST Client / Postman: `tests/http/jwt-auth.http`

## Лабораторна робота 9

Авторизація маршрутів за допомогою JWT (Bearer Token) та перевірка прав доступу (diff authorities):
- **Bearer Token авторизація (`HTTPBearer`)**: у `src/controllers/dependencies.py` налаштовано вилучення та валідацію JWT-токена із заголовка `Authorization: Bearer <token>`.
- **Контроль доступу на рівні методів (RBAC / authorities)**: фабрика залежностей `require_roles(*allowed_roles)` перевіряє роль користувача, вилучену з валідного JWT, забезпечуючи повернення `200 OK` (якщо права є) або `403 Forbidden` (якщо прав недостатньо). Усі запити без токена повертають `401 Unauthorized`.
- **10 сценаріїв тестування доступу (10 скріншотів для GitHub)**:
  - Файл для REST Client / Postman: `tests/http/jwt-authorities.http`
  - Автоматизовані тести pytest: `tests/test_jwt_authorities.py`
  - Папка зі скріншотами: `docs/screenshots/`

### Зведена таблиця 10 запитів доступу:

| № | Метод та URL | Авторизація | Очікуваний статус | Опис сценарію | Скріншот |
|:---:|---|---|:---:|---|:---:|
| **1** | `POST /api/v1/auth/login` | Body: `admin:admin` | `200 OK` | Отримання токена для ADMIN (authorities: `["ADMIN"]`) | ![01](docs/screenshots/01_login_admin.png) |
| **2** | `POST /api/v1/auth/login` | Body: `user:user` | `200 OK` | Отримання токена для USER (authorities: `["USER"]`) | ![02](docs/screenshots/02_login_user.png) |
| **3** | `GET /api/v1/hello/admin` | `Bearer <ADMIN_TOKEN>` | `200 OK` | Доступ адміністратора до admin-ендпоінта | ![03](docs/screenshots/03_hello_admin_with_admin_200.png) |
| **4** | `GET /api/v1/hello/admin` | `Bearer <USER_TOKEN>` | `403 Forbidden` | Заборона доступу користувачу `USER` до admin-ендпоінта | ![04](docs/screenshots/04_hello_admin_with_user_403.png) |
| **5** | `GET /api/v1/hello/user` | `Bearer <USER_TOKEN>` | `200 OK` | Доступ користувача до user-ендпоінта | ![05](docs/screenshots/05_hello_user_with_user_200.png) |
| **6** | `GET /api/v1/hello/user` | `Bearer <ADMIN_TOKEN>` | `403 Forbidden` | Заборона доступу адміністратору до user-only ендпоінта | ![06](docs/screenshots/06_hello_user_with_admin_403.png) |
| **7** | `GET /api/v1/hello/man` | `Bearer <USER_TOKEN>` | `200 OK` | Доступ `USER` до спільного ендпоінта (`USER`, `ADMIN`) | ![07](docs/screenshots/07_hello_man_with_user_200.png) |
| **8** | `GET /api/v1/hello/man` | `Bearer <ADMIN_TOKEN>` | `200 OK` | Доступ `ADMIN` до спільного ендпоінта (`USER`, `ADMIN`) | ![08](docs/screenshots/08_hello_man_with_admin_200.png) |
| **9** | `GET /api/v1/hello/unknown` | `Bearer <USER_TOKEN>` | `200 OK` | Доступ будь-якого автентифікованого користувача | ![09](docs/screenshots/09_hello_unknown_with_user_200.png) |
| **10** | `GET /api/v1/hello/admin` | *Без токена* | `401 Unauthorized` | Заборона доступу для анонімного запиту | ![10](docs/screenshots/10_hello_admin_without_token_401.png) |







