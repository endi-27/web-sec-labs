from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.models.book import Book, BookCreate, BookResponse, BookUpdate
from src.services.auth_service import CurrentUserDep
from src.services.book_service import BookService, get_book_service

router = APIRouter(prefix="/books", tags=["Books"])


@router.get(
    "",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Отримати список усіх книг",
    description="Повертає повний список збережених книг.",
)
def get_all_books(
    service: Annotated[BookService, Depends(get_book_service)],
) -> list[Book]:
    """Отримання всіх книг."""
    return service.get_all()


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Отримати книгу за ідентифікатором",
    description="Повертає одну книгу за її унікальним ID.",
)
def get_book_by_id(
    book_id: Annotated[str, Path(description="ID книги", examples=["1"])],
    service: Annotated[BookService, Depends(get_book_service)],
) -> Book:
    """Отримання однієї книги за ID."""
    book = service.get_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книгу з ID '{book_id}' не знайдено",
        )
    return book


@router.post(
    "",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створити нову книгу",
    description="Створює новий запис книги та повертає його з присвоєним ID (вимагає авторизації).",
)
def create_book(
    book_in: BookCreate,
    current_user: CurrentUserDep,
    service: Annotated[BookService, Depends(get_book_service)],
) -> Book:
    """Створення нової книги (доступно лише авторизованим користувачам)."""
    _ = current_user
    return service.create(book_in)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Оновити книгу за ідентифікатором",
    description="Оновлює вказані поля книги за її ID (вимагає авторизації).",
)
def update_book(
    book_id: Annotated[str, Path(description="ID книги для оновлення", examples=["1"])],
    book_in: BookUpdate,
    current_user: CurrentUserDep,
    service: Annotated[BookService, Depends(get_book_service)],
) -> Book:
    """Оновлення книги за ID (доступно лише авторизованим користувачам)."""
    _ = current_user
    updated = service.update(book_id, book_in)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книгу з ID '{book_id}' не знайдено",
        )
    return updated


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити книгу за ідентифікатором",
    description="Видаляє книгу з репозиторію за її ID (вимагає авторизації).",
)
def delete_book(
    book_id: Annotated[str, Path(description="ID книги для видалення", examples=["1"])],
    current_user: CurrentUserDep,
    service: Annotated[BookService, Depends(get_book_service)],
) -> None:
    """Видалитися книга за ID може лише авторизованим користувачем."""
    _ = current_user
    deleted = service.delete(book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книгу з ID '{book_id}' не знайдено",
        )
