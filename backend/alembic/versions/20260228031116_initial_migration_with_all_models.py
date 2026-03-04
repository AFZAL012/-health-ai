"""Initial migration with all models

Revision ID: 20260228031116
Revises: 
Create Date: 2026-02-28 03:11:16.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260228031116'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all database tables."""
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('role', sa.String(length=50), nullable=False, server_default=sa.text("'user'")),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('medical_history', sa.JSON(), nullable=True),
        sa.Column('emergency_contact', sa.JSON(), nullable=True),
        sa.Column('language_preference', sa.String(length=10), nullable=False, server_default=sa.text("'en'")),
        sa.Column('theme_preference', sa.String(length=10), nullable=False, server_default=sa.text("'light'")),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint('age > 0 AND age < 150', name='valid_age'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    
    # Create diseases table
    op.create_table(
        'diseases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(length=20), nullable=True),
        sa.Column('common_symptoms', sa.JSON(), nullable=True),
        sa.Column('specialist', sa.String(length=100), nullable=True),
        sa.Column('precautions', sa.JSON(), nullable=True),
        sa.Column('lifestyle_recommendations', sa.JSON(), nullable=True),
        sa.Column('urgency_guidelines', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_diseases_name'), 'diseases', ['name'], unique=True)
    
    # Create symptoms table
    op.create_table(
        'symptoms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('canonical_name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('synonyms', sa.JSON(), nullable=True),
        sa.Column('related_symptoms', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('canonical_name')
    )
    op.create_index(op.f('ix_symptoms_canonical_name'), 'symptoms', ['canonical_name'], unique=True)
    
    # Create disease_translations table
    op.create_table(
        'disease_translations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.Integer(), nullable=False),
        sa.Column('language_code', sa.String(length=10), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('precautions', sa.JSON(), nullable=True),
        sa.Column('lifestyle_recommendations', sa.JSON(), nullable=True),
        sa.Column('urgency_guidelines', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['disease_id'], ['diseases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('disease_id', 'language_code', name='uq_disease_language')
    )
    op.create_index(op.f('ix_disease_translations_disease_id'), 'disease_translations', ['disease_id'], unique=False)
    op.create_index(op.f('ix_disease_translations_language_code'), 'disease_translations', ['language_code'], unique=False)
    
    # Create analyses table
    op.create_table(
        'analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('analysis_id', sa.String(length=36), nullable=False),
        sa.Column('symptoms', sa.JSON(), nullable=False),
        sa.Column('predictions', sa.JSON(), nullable=False),
        sa.Column('risk_level', sa.String(length=20), nullable=False),
        sa.Column('recommendations', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('analysis_id')
    )
    op.create_index(op.f('ix_analyses_analysis_id'), 'analyses', ['analysis_id'], unique=True)
    op.create_index(op.f('ix_analyses_created_at'), 'analyses', ['created_at'], unique=False)
    op.create_index('ix_user_created', 'analyses', ['user_id', 'created_at'], unique=False)
    
    # Create reports table
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('report_id', sa.String(length=36), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=False),
        sa.Column('format', sa.String(length=10), nullable=False, server_default=sa.text("'pdf'")),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('report_id')
    )
    op.create_index(op.f('ix_reports_report_id'), 'reports', ['report_id'], unique=True)


def downgrade() -> None:
    """Drop all database tables."""
    
    # Drop tables in reverse order to respect foreign key constraints
    op.drop_index(op.f('ix_reports_report_id'), table_name='reports')
    op.drop_table('reports')
    
    op.drop_index('ix_user_created', table_name='analyses')
    op.drop_index(op.f('ix_analyses_created_at'), table_name='analyses')
    op.drop_index(op.f('ix_analyses_analysis_id'), table_name='analyses')
    op.drop_table('analyses')
    
    op.drop_index(op.f('ix_disease_translations_language_code'), table_name='disease_translations')
    op.drop_index(op.f('ix_disease_translations_disease_id'), table_name='disease_translations')
    op.drop_table('disease_translations')
    
    op.drop_index(op.f('ix_symptoms_canonical_name'), table_name='symptoms')
    op.drop_table('symptoms')
    
    op.drop_index(op.f('ix_diseases_name'), table_name='diseases')
    op.drop_table('diseases')
    
    op.drop_table('user_profiles')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
