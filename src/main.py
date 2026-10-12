from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.config import settings
from src.controllers.auth_controller import router as auth_router
from src.controllers.book_controller import router as book_router
from src.database import engine


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Життєвий цикл додатку (міграції та seed-дані виконуються через Alembic)."""
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend для лабораторних робіт з курсу 'Безпека веб систем'",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Підключення роутерів
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(book_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["General"], summary="Інформація про сервіс")
def read_root() -> dict[str, str]:
    """Кореневий ендпоінт з базовою інформацією про API."""
    return {
        "message": f"Ласкаво просимо до {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["General"], summary="Перевірка стану сервісу")
def health_check() -> dict[str, str]:
    """Healthcheck ендпоінт для перевірки статусу працездатності."""
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn

    logger.info("Запуск сервера Web Security Labs на http://127.0.0.1:8000")
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
