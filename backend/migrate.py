#!/usr/bin/env python
"""Database migration helper script.

This script provides convenient commands for managing database migrations with Alembic.

Usage:
    python migrate.py upgrade    # Apply all pending migrations
    python migrate.py downgrade  # Rollback one migration
    python migrate.py current    # Show current migration version
    python migrate.py history    # Show migration history
    python migrate.py create "migration message"  # Create a new migration
"""
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from alembic.config import Config
from alembic import command


def get_alembic_config():
    """Get Alembic configuration."""
    # Path to alembic.ini (in project root)
    alembic_ini_path = backend_dir.parent / 'alembic.ini'
    
    if not alembic_ini_path.exists():
        print(f"Error: alembic.ini not found at {alembic_ini_path}")
        sys.exit(1)
    
    config = Config(str(alembic_ini_path))
    return config


def upgrade():
    """Apply all pending migrations."""
    print("Applying migrations...")
    config = get_alembic_config()
    command.upgrade(config, "head")
    print("✓ Migrations applied successfully")


def downgrade():
    """Rollback one migration."""
    print("Rolling back one migration...")
    config = get_alembic_config()
    command.downgrade(config, "-1")
    print("✓ Migration rolled back successfully")


def downgrade_base():
    """Rollback all migrations."""
    print("Rolling back all migrations...")
    config = get_alembic_config()
    command.downgrade(config, "base")
    print("✓ All migrations rolled back successfully")


def current():
    """Show current migration version."""
    config = get_alembic_config()
    command.current(config)


def history():
    """Show migration history."""
    config = get_alembic_config()
    command.history(config)


def create(message):
    """Create a new migration."""
    if not message:
        print("Error: Migration message is required")
        print("Usage: python migrate.py create \"migration message\"")
        sys.exit(1)
    
    print(f"Creating new migration: {message}")
    config = get_alembic_config()
    command.revision(config, message=message, autogenerate=True)
    print("✓ Migration created successfully")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command_name = sys.argv[1].lower()
    
    commands = {
        'upgrade': upgrade,
        'downgrade': downgrade,
        'downgrade-base': downgrade_base,
        'current': current,
        'history': history,
    }
    
    if command_name == 'create':
        message = sys.argv[2] if len(sys.argv) > 2 else None
        create(message)
    elif command_name in commands:
        commands[command_name]()
    else:
        print(f"Unknown command: {command_name}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
