import uuid

from src.models.book import Book, BookCreate, BookUpdate


class BookService:
    def __init__(self) -> None:
        self._books: dict[str, Book] = {}
        self.seed_data()

    def seed_data(self) -> None:
        self._books.clear()
        initial_books = [
            Book(
                id="1",
                title="Web Application Security",
                author="Andrew Hoffman",
                description="Exploitation and Countermeasures for Modern Web Applications",
                price=39.99,
                published_year=2020,
            ),
            Book(
                id="2",
                title="The Web Application Hacker's Handbook",
                author="Dafydd Stuttard, Marcus Pinto",
                description="Finding and Exploiting Security Flaws",
                price=49.99,
                published_year=2011,
            ),
            Book(
                id="3",
                title="API Security in Action",
                author="Neil Madden",
                description="Design and implement secure APIs",
                price=44.99,
                published_year=2020,
            ),
        ]
        for book in initial_books:
            self._books[book.id] = book

    def get_all(self) -> list[Book]:
        """Отримати всі книги."""
        return list(self._books.values())

    def get_by_id(self, book_id: str) -> Book | None:
        """Отримати книгу за її ID."""
        return self._books.get(book_id)

    def create(self, data: BookCreate) -> Book:
        """Створити нову книгу."""
        book_id = str(uuid.uuid4())
        book = Book(
            id=book_id,
            title=data.title,
            author=data.author,
            description=data.description,
            price=data.price,
            published_year=data.published_year,
        )
        self._books[book_id] = book
        return book

    def update(self, book_id: str, data: BookUpdate) -> Book | None:
        """Оновити існуючу книгу."""
        existing = self._books.get(book_id)
        if existing is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        updated_book = existing.model_copy(update=update_data)
        self._books[book_id] = updated_book
        return updated_book

    def delete(self, book_id: str) -> bool:
        """Видалити книгу за її ID."""
        if book_id in self._books:
            del self._books[book_id]
            return True
        return False


_book_service_instance = BookService()


def get_book_service() -> BookService:
    return _book_service_instance
