from collections.abc import Callable, Coroutine
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from src.models.user import UserResponse, UserRole
from src.services.auth_service import AuthServiceDep

http_basic = HTTPBasic(auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    basic_credentials: Annotated[HTTPBasicCredentials | None, Depends(http_basic)],
    bearer_credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
    auth_service: AuthServiceDep,
) -> UserResponse:
    """Перевіряє, що користувач авторизований (через Basic Auth або Bearer JWT)."""
    if basic_credentials is not None:
        user = await auth_service.authenticate_user(
            basic_credentials.username,
            basic_credentials.password,
        )
        if user is not None:
            return user

    if bearer_credentials is not None:
        user = await auth_service.verify_token(bearer_credentials.credentials)
        if user is not None:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Необхідна авторизація для доступу до цього ресурсу",
        headers={"WWW-Authenticate": "Basic, Bearer"},
    )


CurrentUserDep = Annotated[UserResponse, Depends(get_current_user)]


def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., Coroutine[Any, Any, UserResponse]]:
    """Фабрика залежностей для динамічної перевірки ролі користувача на ендпоінті."""

    async def role_checker(current_user: CurrentUserDep) -> UserResponse:
        if current_user.role not in allowed_roles:
            allowed_str = ", ".join(role.value for role in allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Доступ заборонено: роль '{current_user.role.value}' не входить до дозволених ({allowed_str})"
                ),
            )
        return current_user

    return role_checker
