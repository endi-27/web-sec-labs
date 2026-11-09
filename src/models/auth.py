from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from src.models.user import UserRole


class LoginRequest(BaseModel):
    """Схема запиту на вхід у систему (підтримує username, email або login)."""

    username: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="Ім'я користувача, логін або email",
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

    @model_validator(mode="before")
    @classmethod
    def normalize_credentials(cls, data: object) -> object:
        if isinstance(data, dict) and "username" not in data:
            if "email" in data:
                data["username"] = data["email"]
            elif "login" in data:
                data["username"] = data["login"]
        return data


class TokenResponse(BaseModel):
    """Схема відповіді після успішного входу (JWT токен)."""

    token: Annotated[
        str,
        Field(description="JWT токен (сумісність із форматом лабораторної викладача)"),
    ]
    access_token: Annotated[
        str,
        Field(description="JWT токен у стандартному форматі OAuth2/Bearer"),
    ]
    token_type: Annotated[
        str,
        Field(default="bearer", description="Тип токена авторизації"),
    ] = "bearer"
    username: Annotated[
        str,
        Field(description="Ім'я користувача або email"),
    ]
    role: Annotated[
        UserRole,
        Field(description="Роль користувача у системі"),
    ]
    authorities: Annotated[
        list[str],
        Field(default_factory=list, description="Список прав/ролей у форматі authorities"),
    ]
