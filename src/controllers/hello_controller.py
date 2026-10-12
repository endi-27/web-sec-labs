from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.controllers.dependencies import (
    CurrentUserDep,
    get_current_user,
    require_roles,
)
from src.models.user import UserResponse, UserRole

router = APIRouter(
    prefix="/hello",
    tags=["Hello"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/admin",
    status_code=status.HTTP_200_OK,
    summary="Привітання для ролі ADMIN",
)
async def hello_admin(
    current_user: Annotated[UserResponse, Depends(require_roles(UserRole.ADMIN))],
) -> dict[str, str]:
    """Доступно лише користувачам із роллю ADMIN."""
    return {
        "message": "Hello Admin!",
        "username": current_user.username,
        "role": current_user.role.value,
    }


@router.get(
    "/user",
    status_code=status.HTTP_200_OK,
    summary="Привітання для ролі USER",
)
async def hello_user(
    current_user: Annotated[UserResponse, Depends(require_roles(UserRole.USER))],
) -> dict[str, str]:
    """Доступно лише користувачам із роллю USER."""
    return {
        "message": "Hello!, user",
        "username": current_user.username,
        "role": current_user.role.value,
    }


@router.get(
    "/man",
    status_code=status.HTTP_200_OK,
    summary="Привітання для ролей USER або ADMIN",
)
async def hello_man(
    current_user: Annotated[UserResponse, Depends(require_roles(UserRole.USER, UserRole.ADMIN))],
) -> dict[str, str]:
    """Доступно користувачам із ролями USER або ADMIN."""
    return {
        "message": "Hello, man!",
        "username": current_user.username,
        "role": current_user.role.value,
    }


@router.get(
    "/superadmin",
    status_code=status.HTTP_200_OK,
    summary="Привітання для ролі SUPERADMIN",
)
async def hello_superadmin(
    current_user: Annotated[UserResponse, Depends(require_roles(UserRole.SUPERADMIN))],
) -> dict[str, str]:
    """Доступно лише користувачам із роллю SUPERADMIN."""
    return {
        "message": "Hello Superadmin!",
        "username": current_user.username,
        "role": current_user.role.value,
    }


@router.get(
    "/unknown",
    status_code=status.HTTP_200_OK,
    summary="Привітання для будь-якого авторизованого користувача",
)
async def hello_unknown(
    current_user: CurrentUserDep,
) -> dict[str, str]:
    """Доступно будь-якому авторизованому користувачу (USER, ADMIN, SUPERADMIN)."""
    return {
        "message": "Hello Unknown!",
        "username": current_user.username,
        "role": current_user.role.value,
    }
