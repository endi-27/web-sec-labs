from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.models.book import BookCreate, BookORM, BookResponse, BookUpdate
from src.services.auth_service import CurrentUserDep, get_current_user
from src.services.book_service import BookServiceDep

# Аналог SecurityConfig: auth.anyRequest().authenticated() для роутера книг
router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Отримати список усіх книг",
    description="Повертає повний список збережених у БД книг (вимагає авторизації).",
)
async def get_all_books(
    service: BookServiceDep,
) -> list[BookORM]:
    """Отримання всіх книг із PostgreSQL."""
    return await service.get_all()


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Отримати книгу за ідентифікатором",
    description="Повертає одну книгу за її унікальним ID (вимагає авторизації).",
)
async def get_book_by_id(
    book_id: Annotated[str, Path(description="ID книги", examples=["1"])],
    service: BookServiceDep,
) -> BookORM:
    """Отримання однієї книги за ID із PostgreSQL."""
    book = await service.get_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книгу з ID '{book_id}' не знайдено",
        )
    return book


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Створити нову книгу",
    description="Створює новий запис книги в PostgreSQL із метаданими аудиту (вимагає авторизації).",
)
async def create_book(
    book_in: BookCreate,
    current_user: CurrentUserDep,
    service: BookServiceDep,
) -> BookORM:
    """Створення нової книги з фіксацією автора (created_by) в аудиті."""
    return await service.create(book_in, auditor=current_user.username)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Оновити книгу за ідентифікатором",
    description="Оновлює поля книги в PostgreSQL та інкрементує version (вимагає авторизації).",
)
async def update_book(
    book_id: Annotated[str, Path(description="ID книги для оновлення", examples=["1"])],
    book_in: BookUpdate,
    current_user: CurrentUserDep,
    service: BookServiceDep,
) -> BookORM:
    """Оновлення книги за ID із фіксацією last_modified_by та інкрементом version."""
    updated = await service.update(book_id, book_in, auditor=current_user.username)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книгу з ID '{book_id}' не знайдено",
        )
    return updated


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    summary="Видалити книгу за ідентифікатором",
    description="Видаляє книгу з PostgreSQL за її ID (вимагає авторизації).",
)
async def delete_book(
    book_id: Annotated[str, Path(description="ID книги для видалення", examples=["1"])],
    service: BookServiceDep,
) -> None:
    """Видалення книги за ID."""
    deleted = await service.delete(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книгу з ID '{book_id}' не знайдено",
        )
