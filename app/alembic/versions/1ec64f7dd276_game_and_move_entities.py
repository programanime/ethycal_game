"""game and move entities

Revision ID: 1ec64f7dd276
Revises: 
Create Date: 2024-04-18 14:05:12.140912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1ec64f7dd276"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_games")),
    )
    op.create_table(
        "moves",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("is_machine_move", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["game_id"], ["games.id"], name=op.f("fk_moves_game_id_games")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_moves")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("moves")
    op.drop_table("games")
    # ### end Alembic commands ###
