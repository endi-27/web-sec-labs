from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status

from src.config import settings
from src.models.auth import TokenResponse
from src.models.user import UserResponse, UserRole
from src.repositories.user_repository import UserRepository, UserRepositoryDep


class AuthService:
    """Сервіс автентифікації та роботи з користувачами у PostgreSQL (BCrypt + JWT)."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Хешування пароля за допомогою BCrypt."""
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Перевірка пароля за допомогою BCrypt."""
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                hashed_password.encode("utf-8"),
            )
        except ValueError:
            return False

    async def authenticate_user(self, username: str, password: str) -> UserResponse | None:
        """Перевірка логіна та пароля користувача за таблицею users у PostgreSQL."""
        user = await self._user_repository.find_by_username(username)
        if user is None:
            return None
        if not self.verify_password(password, user.password):
            return None
        return UserResponse.model_validate(user)

    @staticmethod
    def create_access_token(username: str, role: UserRole) -> str:
        """Генерація JWT токена доступу з роллю користувача."""
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=settings.jwt_expire_minutes)
        payload: dict[str, object] = {
            "sub": username,
            "role": role.value,
            "iat": now,
            "exp": expire,
        }
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    async def verify_token(self, token: str) -> UserResponse | None:
        """Валідація JWT токена та отримання актуального користувача з БД."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
            username = payload.get("sub")
            if not isinstance(username, str) or not username:
                return None
            user = await self._user_repository.find_by_username(username)
            if user is None:
                return None
            return UserResponse.model_validate(user)
        except jwt.PyJWTError:
            return None

    async def login(self, username: str, password: str) -> TokenResponse:
        """Автентифікація користувача та видача JWT токена."""
        user = await self.authenticate_user(username, password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невірний логін або пароль",
                headers={"WWW-Authenticate": "Basic, Bearer"},
            )
        token = self.create_access_token(user.username, user.role)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            username=user.username,
            role=user.role,
        )


def get_auth_service(user_repository: UserRepositoryDep) -> AuthService:
    return AuthService(user_repository)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
