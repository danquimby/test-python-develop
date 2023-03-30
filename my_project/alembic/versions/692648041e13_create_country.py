"""create_country

Revision ID: 692648041e13
Revises: d8f4c9f632ef
Create Date: 2023-03-29 16:49:24.402486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "692648041e13"
down_revision = "d8f4c9f632ef"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "countries",
        sa.Column(
            "user_id", sa.BigInteger(), sa.Identity(always=True), nullable=False
        ),
        sa.Column(
            "create_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_index(op.f("ix_countries_name"), "countries", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_countries_name"), table_name="countries")
    op.drop_table("countries")
    # ### end Alembic commands ###
