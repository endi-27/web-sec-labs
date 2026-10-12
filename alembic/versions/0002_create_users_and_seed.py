"""create users table and seed 3 users with roles and bcrypt passwords

Revision ID: 0002_create_users
Revises: 0001_initial_books
Create Date: 2026-10-12 15:15:00.000000

"""
from collections.abc import Sequence
from datetime import UTC, datetime

from alembic import op
import bcrypt
import sqlalchemy as sa

revision: str = "0002_create_users"
down_revision: str | None = "0001_initial_books"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt(rounds=4)).decode("utf-8")


ADMIN_PASSWORD_HASH = _hash_password("admin")
USER_PASSWORD_HASH = _hash_password("user")
SUPERADMIN_PASSWORD_HASH = _hash_password("superadmin")



def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS users CASCADE")
    users_table = op.create_table(
        "users",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_modified_by", sa.String(length=100), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    now = datetime.now(UTC)
    op.bulk_insert(
        users_table,
        [
            {
                "id": "1",
                "username": "admin",
                "password": ADMIN_PASSWORD_HASH,
                "role": "ADMIN",
                "created_date": now,
                "created_by": "System",
                "last_modified_date": now,
                "last_modified_by": "System",
                "version": 1,
            },
            {
                "id": "2",
                "username": "user",
                "password": USER_PASSWORD_HASH,
                "role": "USER",
                "created_date": now,
                "created_by": "System",
                "last_modified_date": now,
                "last_modified_by": "System",
                "version": 1,
            },
            {
                "id": "3",
                "username": "superadmin",
                "password": SUPERADMIN_PASSWORD_HASH,
                "role": "SUPERADMIN",
                "created_date": now,
                "created_by": "System",
                "last_modified_date": now,
                "last_modified_by": "System",
                "version": 1,
            },

        ],
    )


def downgrade() -> None:
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
