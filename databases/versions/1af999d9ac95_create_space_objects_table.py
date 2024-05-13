"""create space objects table

Revision ID: 1af999d9ac95
Revises: 
Create Date: 2024-04-30 14:56:27.271420

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1af999d9ac95"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "space_objects_catalog"


def upgrade() -> None:
    op.create_table(
        TABLE_NAME,
        sa.Column("sat_id", sa.String(128), nullable=False, primary_key=True),
        sa.Column("sat_catalog_number", sa.String(128), nullable=False),
        sa.Column("sat_name", sa.String(128), nullable=False),
        sa.Column("file_id", sa.String(128), nullable=False),
        sa.Column("launch_country", sa.String(128), nullable=False),
        sa.Column("launch_site", sa.String(128), nullable=False),
        sa.Column("launch_date", sa.String(128), nullable=False),
        sa.Column("launch_year", sa.String(128), nullable=False),
        sa.Column("launch_number", sa.String(128), nullable=False),
        sa.Column("launch_piece", sa.String(128), nullable=False),
        sa.Column("object_type", sa.String(128), nullable=False),
        sa.Column("object_name", sa.String(128), nullable=False),
        sa.Column("object_id", sa.String(128), nullable=False),
        sa.Column("object_number", sa.String(128), nullable=False),
        sa.Column("date_created", sa.DateTime, nullable=False),
        sa.Column("date_modified", sa.DateTime, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table(TABLE_NAME)
    pass
