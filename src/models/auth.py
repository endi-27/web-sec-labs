from typing import Annotated

from pydantic import BaseModel, Field

from src.models.user import UserRole


class LoginRequest(BaseModel):
    """Схема запиту на вхід у систему."""

    username: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="Ім'я користувача",
            examples=["admin"],
        ),
    ]
    password: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="Пароль користувача",
            examples=["admin"],
        ),
    ]


class TokenResponse(BaseModel):
    """Схема відповіді після успішного входу (JWT токен)."""

    access_token: str
    token_type: str = "bearer"
    username: str
    role: UserRole
