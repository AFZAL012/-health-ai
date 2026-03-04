# Database Migration Guide

This guide explains how to use Alembic for database migrations in the Medical Diagnosis Enhancement project.

## Quick Start

### Prerequisites

1. **Start the database**:
   ```bash
   docker compose up -d postgres
   ```

2. **Verify database is running**:
   ```bash
   docker compose ps
   ```

### Apply Migrations

```bash
# Using the helper script (recommended)
python backend/migrate.py upgrade

# Or using Alembic directly
python -m alembic upgrade head
```

### Verify Setup

```bash
# Run the test script
python backend/test_migration.py
```

## What Was Set Up

### 1. Alembic Configuration

- **alembic.ini**: Main configuration file in project root
- **backend/alembic/env.py**: Environment configuration that integrates with Flask app
- **backend/alembic/versions/**: Directory containing migration scripts

### 2. Initial Migration

The initial migration (`20260228031116_initial_migration_with_all_models.py`) creates all database tables:

#### Tables Created

1. **users** - User accounts and authentication
   - Columns: id, email, password_hash, created_at, updated_at, is_active, is_verified, role
   - Indexes: email (unique)

2. **user_profiles** - User demographics and preferences
   - Columns: id, user_id, age, gender, medical_history, emergency_contact, language_preference, theme_preference
   - Foreign Key: user_id → users.id (CASCADE delete)
   - Constraints: age > 0 AND age < 150

3. **diseases** - Disease information database
   - Columns: id, name, description, severity, common_symptoms, specialist, precautions, lifestyle_recommendations, urgency_guidelines
   - Indexes: name (unique)

4. **symptoms** - Symptom catalog with synonyms
   - Columns: id, canonical_name, category, synonyms, related_symptoms
   - Indexes: canonical_name (unique)

5. **disease_translations** - Multi-language disease information
   - Columns: id, disease_id, language_code, name, description, precautions, lifestyle_recommendations, urgency_guidelines
   - Foreign Key: disease_id → diseases.id (CASCADE delete)
   - Unique Constraint: (disease_id, language_code)
   - Indexes: disease_id, language_code

6. **analyses** - Symptom analysis records
   - Columns: id, user_id, analysis_id, symptoms, predictions, risk_level, recommendations, created_at, notes
   - Foreign Key: user_id → users.id (SET NULL on delete)
   - Indexes: analysis_id (unique), created_at, (user_id, created_at)

7. **reports** - Generated PDF reports
   - Columns: id, report_id, analysis_id, format, file_path, file_size, created_at, expires_at
   - Foreign Key: analysis_id → analyses.id (CASCADE delete)
   - Indexes: report_id (unique)

### 3. Helper Scripts

- **backend/migrate.py**: Convenient wrapper for common Alembic commands
- **backend/test_migration.py**: Test script to verify migration setup

## Common Operations

### Apply All Migrations

```bash
python backend/migrate.py upgrade
```

This applies all pending migrations to bring the database to the latest version.

### Rollback One Migration

```bash
python backend/migrate.py downgrade
```

This rolls back the most recent migration.

### Rollback All Migrations

```bash
python backend/migrate.py downgrade-base
```

This rolls back all migrations, dropping all tables.

### Check Current Version

```bash
python backend/migrate.py current
```

Shows the current migration version applied to the database.

### View Migration History

```bash
python backend/migrate.py history
```

Shows all available migrations and their status.

### Create New Migration

When you modify database models:

```bash
python backend/migrate.py create "Add new column to users"
```

This generates a new migration file based on model changes.

## Testing Migrations

### Manual Testing

1. **Test upgrade**:
   ```bash
   python backend/migrate.py upgrade
   ```

2. **Verify tables exist**:
   ```bash
   docker compose exec postgres psql -U meduser -d medical_diagnosis -c "\dt"
   ```

3. **Test downgrade**:
   ```bash
   python backend/migrate.py downgrade-base
   ```

4. **Verify tables dropped**:
   ```bash
   docker compose exec postgres psql -U meduser -d medical_diagnosis -c "\dt"
   ```

5. **Test re-upgrade**:
   ```bash
   python backend/migrate.py upgrade
   ```

### Automated Testing

Run the comprehensive test script:

```bash
python backend/test_migration.py
```

This script tests:
- Database connection
- Alembic configuration
- Migration upgrade
- Migration downgrade
- Migration reapply

## Workflow for Model Changes

1. **Modify the model** in `backend/models/`:
   ```python
   # Example: Add a new column to User model
   class User(BaseModel):
       # ... existing columns ...
       last_login = db.Column(db.DateTime, nullable=True)
   ```

2. **Generate migration**:
   ```bash
   python backend/migrate.py create "Add last_login to users"
   ```

3. **Review the generated migration** in `backend/alembic/versions/`:
   - Check that the changes are correct
   - Add any manual data migrations if needed
   - Verify the downgrade function

4. **Test the migration**:
   ```bash
   # Apply migration
   python backend/migrate.py upgrade
   
   # Verify it works
   # ... test your application ...
   
   # Test rollback
   python backend/migrate.py downgrade
   
   # Reapply
   python backend/migrate.py upgrade
   ```

5. **Commit the migration**:
   ```bash
   git add backend/alembic/versions/*.py
   git commit -m "Add last_login column to users table"
   ```

## Environment Configuration

The database URL is determined in this order:

1. **DATABASE_URL environment variable** (highest priority):
   ```bash
   export DATABASE_URL="postgresql://user:pass@host:port/dbname"
   ```

2. **Flask app configuration** (from config.py)

3. **Default value**:
   ```
   postgresql://meduser:medpass_dev@localhost:5432/medical_diagnosis
   ```

## Troubleshooting

### Database Connection Failed

**Problem**: Can't connect to PostgreSQL

**Solutions**:
1. Check if database is running:
   ```bash
   docker compose ps
   ```

2. Start the database:
   ```bash
   docker compose up -d postgres
   ```

3. Check database logs:
   ```bash
   docker compose logs postgres
   ```

4. Verify connection string:
   ```bash
   echo $DATABASE_URL
   ```

### Table Already Exists

**Problem**: Migration fails with "relation already exists"

**Solutions**:
1. Check current migration version:
   ```bash
   python backend/migrate.py current
   ```

2. If tables exist but no migrations applied, stamp the database:
   ```bash
   python -m alembic stamp head
   ```

3. Or drop all tables and reapply:
   ```bash
   python backend/migrate.py downgrade-base
   python backend/migrate.py upgrade
   ```

### Autogenerate Doesn't Detect Changes

**Problem**: Creating a migration doesn't detect model changes

**Solutions**:
1. Ensure models are imported in `backend/models/__init__.py`
2. Verify models inherit from `db.Model` or `BaseModel`
3. Check that the model file is saved
4. Try creating a manual migration:
   ```bash
   python -m alembic revision -m "Manual migration"
   ```

### Migration Conflicts

**Problem**: Multiple developers created migrations with same revision

**Solutions**:
1. Use Alembic's merge command:
   ```bash
   python -m alembic merge -m "Merge migrations" <rev1> <rev2>
   ```

2. Or manually resolve by editing migration files

## Best Practices

1. **Always review autogenerated migrations** - Alembic may not detect all changes
2. **Test migrations before committing** - Run upgrade and downgrade
3. **Keep migrations small** - One logical change per migration
4. **Never modify applied migrations** - Create a new migration instead
5. **Backup production database** before applying migrations
6. **Use transactions** - Migrations run in transactions by default
7. **Document complex migrations** - Add comments explaining non-obvious changes

## Production Deployment

### Pre-Deployment Checklist

- [ ] All migrations tested in development
- [ ] Database backup created
- [ ] Downgrade path tested
- [ ] Migration time estimated
- [ ] Maintenance window scheduled (if needed)

### Deployment Steps

1. **Backup database**:
   ```bash
   pg_dump -U meduser -d medical_diagnosis > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Apply migrations**:
   ```bash
   python backend/migrate.py upgrade
   ```

3. **Verify application**:
   - Check application logs
   - Test critical functionality
   - Monitor error rates

4. **Rollback if needed**:
   ```bash
   python backend/migrate.py downgrade
   ```

## References

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- Project Requirements: `.kiro/specs/medical-diagnosis-enhancement/requirements.md` (Requirement 17.5)
