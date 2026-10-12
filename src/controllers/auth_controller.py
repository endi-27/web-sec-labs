from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials

from src.models.auth import LoginRequest, TokenResponse
from src.services.auth_service import (
    AuthService,
    get_auth_service,
    http_basic,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Вхід у систему (отримання JWT токена)",
    description="Автентифікація за логіном/паролем (JSON або Basic Auth) та видача токена.",
)
def login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    basic_credentials: Annotated[HTTPBasicCredentials | None, Depends(http_basic)] = None,
    credentials: Annotated[LoginRequest | None, Body()] = None,
) -> TokenResponse:
    """Ендпоінт входу за адресою /api/v1/auth/login."""
    if credentials is not None:
        return auth_service.login(credentials.username, credentials.password)
    if basic_credentials is not None:
        return auth_service.login(basic_credentials.username, basic_credentials.password)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не передано облікові дані для входу",
        headers={"WWW-Authenticate": "Basic, Bearer"},
    )
