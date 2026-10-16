"""initial assets table

Revision ID: 001_initial
Revises: 
Create Date: 2026-10-16 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("serial_number", sa.String(), unique=True, nullable=False),
        sa.Column("status", sa.String(), server_default="Available"),
    )

def downgrade() -> None:
    op.drop_table("assets")