"""add search_vector trigger

Revision ID: 95549847d413
Revises: c403d6e2afc3
Create Date: 2025-03-24 00:51:21.210936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '95549847d413'
down_revision: Union[str, None] = 'c403d6e2afc3'
branch_labels: None
depends_on: None


def upgrade() -> None:
    # Create GIN index
    op.execute("CREATE INDEX apps_search_vector_idx ON apps USING GIN (search_vector)")

    # Remove função antiga, se existir
    op.execute("DROP FUNCTION IF EXISTS update_search_vector")

    # Cria nova função usando concat_ws
    op.execute("""
        CREATE FUNCTION update_search_vector() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector('english',
                concat_ws(' ', NEW.name, NEW.subtitle, NEW.developer, NEW.description)
            );
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)

    # Cria trigger para manter search_vector atualizado
    op.execute("""
        CREATE TRIGGER tsvectorupdate
        BEFORE INSERT OR UPDATE ON apps
        FOR EACH ROW EXECUTE FUNCTION update_search_vector();
    """)



def downgrade():
    op.execute("DROP TRIGGER tsvectorupdate ON apps")
    op.execute("DROP FUNCTION update_search_vector")
    op.execute("DROP INDEX apps_search_vector_idx")
    op.drop_column('apps', 'search_vector')