"""create books table and seed initial data

Revision ID: 0001_initial_books
Revises:
Create Date: 2026-10-12 14:30:00.000000

"""
from collections.abc import Sequence
from datetime import UTC, datetime

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_books"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS books CASCADE")
    books_table = op.create_table(
        "books",

        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("author", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("published_year", sa.Integer(), nullable=True),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(length=100), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_modified_by", sa.String(length=100), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    now = datetime.now(UTC)
    op.bulk_insert(
        books_table,
        [
            {
                "id": "1",
                "title": "Web Application Security",
                "author": "Andrew Hoffman",
                "description": "Exploitation and Countermeasures for Modern Web Applications",
                "price": 39.99,
                "published_year": 2020,
                "created_date": now,
                "created_by": "Admin",
                "last_modified_date": now,
                "last_modified_by": "Admin",
                "version": 1,
            },
            {
                "id": "2",
                "title": "The Web Application Hacker's Handbook",
                "author": "Dafydd Stuttard, Marcus Pinto",
                "description": "Finding and Exploiting Security Flaws",
                "price": 49.99,
                "published_year": 2011,
                "created_date": now,
                "created_by": "Admin",
                "last_modified_date": now,
                "last_modified_by": "Admin",
                "version": 1,
            },
            {
                "id": "3",
                "title": "API Security in Action",
                "author": "Neil Madden",
                "description": "Design and implement secure APIs",
                "price": 44.99,
                "published_year": 2020,
                "created_date": now,
                "created_by": "Admin",
                "last_modified_date": now,
                "last_modified_by": "Admin",
                "version": 1,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("books")
