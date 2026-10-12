from src.controllers.auth_controller import router as auth_router
from src.controllers.book_controller import router as book_router
from src.controllers.dependencies import (
    CurrentUserDep,
    get_current_user,
    require_roles,
)
from src.controllers.hello_controller import router as hello_router

__all__ = [
    "auth_router",
    "book_router",
    "hello_router",
    "CurrentUserDep",
    "get_current_user",
    "require_roles",
]
