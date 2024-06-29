"""Make user_id nullable in documents

Revision ID: 64e25bc9ff4a
Revises: 
Create Date: 2024-06-28 17:56:42.987926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64e25bc9ff4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create a new temporary table with the modified schema
    op.create_table('new_document',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('upload_date', sa.DateTime, server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=True),
        sa.Column('questions', sa.relationship('Question', backref='document', lazy=True))
    )
    
    # Copy data from the old table to the new table
    op.execute('INSERT INTO new_document (id, filename, upload_date, user_id) SELECT id, filename, upload_date, user_id FROM document')
    
    # Drop the old table
    op.drop_table('document')
    
    # Rename the new table to the original table name
    op.rename_table('new_document', 'document')

def downgrade():
    # Similar steps in reverse to restore the original schema
    op.create_table('old_document',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('upload_date', sa.DateTime, server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    )
    
    op.execute('INSERT INTO old_document (id, filename, upload_date, user_id) SELECT id, filename, upload_date, user_id FROM document')
    op.drop_table('document')
    op.rename_table('old_document', 'document')