from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.controllers.dependencies import (
    CurrentUserDep,
    get_current_user,
    require_roles,
)
from src.models.book import BookCreate, BookORM, BookResponse, BookUpdate
from src.models.user import UserResponse, UserRole
from src.services.book_service import BookServiceDep

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
    description="Повертає список книг (доступно для USER, ADMIN, SUPERADMIN).",
)
async def get_all_books(
    current_user: CurrentUserDep,
    service: BookServiceDep,
) -> list[BookORM]:
    """Отримання всіх книг із PostgreSQL (будь-який авторизований користувач)."""
    _ = current_user
    return await service.get_all()


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Отримати книгу за ідентифікатором",
    description="Повертає одну книгу за її ID (доступно для USER, ADMIN, SUPERADMIN).",
)
async def get_book_by_id(
    book_id: Annotated[str, Path(description="ID книги", examples=["1"])],
    current_user: CurrentUserDep,
    service: BookServiceDep,
) -> BookORM:
    """Отримання однієї книги за ID із PostgreSQL."""
    _ = current_user
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
    description="Створює нову книгу в PostgreSQL (доступно для ADMIN та SUPERADMIN).",
)
async def create_book(
    book_in: BookCreate,
    current_user: Annotated[UserResponse, Depends(require_roles(UserRole.ADMIN, UserRole.SUPERADMIN))],
    service: BookServiceDep,
) -> BookORM:
    """Створення нової книги (дозволено лише ADMIN та SUPERADMIN)."""
    return await service.create(book_in, auditor=current_user.username)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Оновити книгу за ідентифікатором",
    description="Оновлює поля книги в PostgreSQL (доступно для ADMIN та SUPERADMIN).",
)
async def update_book(
    book_id: Annotated[str, Path(description="ID книги для оновлення", examples=["1"])],
    book_in: BookUpdate,
    current_user: Annotated[UserResponse, Depends(require_roles(UserRole.ADMIN, UserRole.SUPERADMIN))],
    service: BookServiceDep,
) -> BookORM:
    """Оновлення книги за ID (дозволено лише ADMIN та SUPERADMIN)."""
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
    description="Видаляє книгу з PostgreSQL (доступно лише для SUPERADMIN).",
)
async def delete_book(
    book_id: Annotated[str, Path(description="ID книги для видалення", examples=["1"])],
    current_user: Annotated[UserResponse, Depends(require_roles(UserRole.SUPERADMIN))],
    service: BookServiceDep,
) -> dict[str, str]:
    """Видалення книги за ID (дозволено лише SUPERADMIN)."""
    deleted = await service.delete(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книгу з ID '{book_id}' не знайдено",
        )
    return {"message": f"Книгу '{book_id}' видалено", "deleted_by": current_user.username}
