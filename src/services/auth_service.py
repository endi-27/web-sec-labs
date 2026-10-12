import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from src.config import settings
from src.models.auth import TokenResponse, UserResponse

http_basic = HTTPBasic(auto_error=False)
http_bearer = HTTPBearer(auto_error=False)


class AuthService:
    """Сервіс автентифікації та авторизації користувачів."""

    def authenticate_user(self, username: str, password: str) -> UserResponse | None:
        """Перевірка логіна та пароля (захист від timing-атак через compare_digest)."""
        is_correct_username = secrets.compare_digest(
            username.encode("utf-8"),
            settings.security_user_name.encode("utf-8"),
        )
        is_correct_password = secrets.compare_digest(
            password.encode("utf-8"),
            settings.security_user_password.encode("utf-8"),
        )
        if not (is_correct_username and is_correct_password):
            return None
        return UserResponse(username=settings.security_user_name, role="ADMIN")

    def create_access_token(self, username: str) -> str:
        """Генерація JWT токена доступу."""
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=settings.jwt_expire_minutes)
        payload: dict[str, object] = {
            "sub": username,
            "role": "ADMIN",
            "iat": now,
            "exp": expire,
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    def verify_token(self, token: str) -> UserResponse | None:
        """Валідація JWT токена."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            username = payload.get("sub")
            role = payload.get("role", "ADMIN")
            if not isinstance(username, str) or not username:
                return None
            return UserResponse(username=username, role=str(role))
        except jwt.PyJWTError:
            return None

    def login(self, username: str, password: str) -> TokenResponse:
        """Автентифікація користувача та видача токена."""
        user = self.authenticate_user(username, password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний логін або пароль",
                headers={"WWW-Authenticate": "Basic, Bearer"},
            )
        token = self.create_access_token(user.username)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            username=user.username,
        )


_auth_service_instance = AuthService()


def get_auth_service() -> AuthService:
    return _auth_service_instance


def get_current_user(
    basic_credentials: Annotated[HTTPBasicCredentials | None, Depends(http_basic)],
    bearer_credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserResponse:
    """FastAPI-залежність для захисту ендпоінтів (підтримує Basic Auth та Bearer JWT)."""
    if basic_credentials is not None:
        user = auth_service.authenticate_user(
            basic_credentials.username,
            basic_credentials.password,
        )
        if user is not None:
            return user

    if bearer_credentials is not None:
        user = auth_service.verify_token(bearer_credentials.credentials)
        if user is not None:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Необхідна авторизація для доступу до цього ресурсу",
        headers={"WWW-Authenticate": "Basic, Bearer"},
    )


CurrentUserDep = Annotated[UserResponse, Depends(get_current_user)]
