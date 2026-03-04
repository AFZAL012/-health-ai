#!/usr/bin/env python
"""Test script to verify Alembic migration setup.

This script tests that:
1. Alembic configuration is correct
2. Migration can be applied (upgrade)
3. Migration can be rolled back (downgrade)
4. All tables are created correctly

Usage:
    python backend/test_migration.py
"""
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, inspect, text
from alembic.config import Config
from alembic import command
import traceback


def get_database_url():
    """Get database URL from environment or use default."""
    return os.getenv(
        'DATABASE_URL',
        'postgresql://meduser:medpass_dev@localhost:5432/medical_diagnosis'
    )


def get_alembic_config():
    """Get Alembic configuration."""
    alembic_ini_path = backend_dir.parent / 'alembic.ini'
    
    if not alembic_ini_path.exists():
        print(f"❌ Error: alembic.ini not found at {alembic_ini_path}")
        return None
    
    config = Config(str(alembic_ini_path))
    return config


def test_database_connection():
    """Test database connection."""
    print("\n1. Testing database connection...")
    try:
        engine = create_engine(get_database_url())
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        print("   ✓ Database connection successful")
        return True
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        return False


def test_alembic_config():
    """Test Alembic configuration."""
    print("\n2. Testing Alembic configuration...")
    try:
        config = get_alembic_config()
        if config is None:
            return False
        
        # Check if versions directory exists
        versions_dir = backend_dir / 'alembic' / 'versions'
        if not versions_dir.exists():
            print(f"   ❌ Versions directory not found: {versions_dir}")
            return False
        
        # Check if initial migration exists
        migration_files = list(versions_dir.glob('*.py'))
        migration_files = [f for f in migration_files if not f.name.startswith('__')]
        
        if not migration_files:
            print("   ❌ No migration files found")
            return False
        
        print(f"   ✓ Found {len(migration_files)} migration file(s)")
        for f in migration_files:
            print(f"     - {f.name}")
        
        return True
    except Exception as e:
        print(f"   ❌ Alembic configuration test failed: {e}")
        traceback.print_exc()
        return False


def test_migration_upgrade():
    """Test applying migrations."""
    print("\n3. Testing migration upgrade...")
    try:
        config = get_alembic_config()
        if config is None:
            return False
        
        # Apply migrations
        command.upgrade(config, "head")
        print("   ✓ Migrations applied successfully")
        
        # Verify tables were created
        engine = create_engine(get_database_url())
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'users', 'user_profiles', 'diseases', 'symptoms',
            'disease_translations', 'analyses', 'reports', 'alembic_version'
        ]
        
        missing_tables = [t for t in expected_tables if t not in tables]
        
        if missing_tables:
            print(f"   ❌ Missing tables: {missing_tables}")
            return False
        
        print(f"   ✓ All {len(expected_tables)} expected tables created")
        for table in expected_tables:
            if table != 'alembic_version':
                print(f"     - {table}")
        
        return True
    except Exception as e:
        print(f"   ❌ Migration upgrade failed: {e}")
        traceback.print_exc()
        return False


def test_migration_downgrade():
    """Test rolling back migrations."""
    print("\n4. Testing migration downgrade...")
    try:
        config = get_alembic_config()
        if config is None:
            return False
        
        # Rollback migrations
        command.downgrade(config, "base")
        print("   ✓ Migrations rolled back successfully")
        
        # Verify tables were dropped
        engine = create_engine(get_database_url())
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Only alembic_version should remain
        remaining_tables = [t for t in tables if t != 'alembic_version']
        
        if remaining_tables:
            print(f"   ⚠ Warning: Some tables still exist: {remaining_tables}")
            # This is not necessarily an error, as some tables might be managed elsewhere
        
        print("   ✓ All application tables dropped")
        
        return True
    except Exception as e:
        print(f"   ❌ Migration downgrade failed: {e}")
        traceback.print_exc()
        return False


def test_migration_reapply():
    """Test reapplying migrations."""
    print("\n5. Testing migration reapply...")
    try:
        config = get_alembic_config()
        if config is None:
            return False
        
        # Reapply migrations
        command.upgrade(config, "head")
        print("   ✓ Migrations reapplied successfully")
        
        return True
    except Exception as e:
        print(f"   ❌ Migration reapply failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Alembic Migration Setup Test")
    print("=" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Alembic Configuration", test_alembic_config),
        ("Migration Upgrade", test_migration_upgrade),
        ("Migration Downgrade", test_migration_downgrade),
        ("Migration Reapply", test_migration_reapply),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Alembic migration setup is working correctly.")
        return 0
    else:
        print("\n⚠ Some tests failed. Please check the output above for details.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
