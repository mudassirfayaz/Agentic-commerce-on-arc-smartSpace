# Design: Database Setup and Table Creation

## Context
The backend uses PostgreSQL with SQLAlchemy ORM and Alembic for migrations. All data models are already defined in `backend/src/models/`, but no database tables exist yet. We need to create the initial migration and set up the database schema.

## Goals
- Create all database tables from existing SQLAlchemy models
- Ensure proper foreign key relationships and constraints
- Create necessary indexes for performance
- Support PostgreSQL enum types
- Enable future schema changes through Alembic migrations

## Non-Goals
- Database seeding or initial data (separate concern)
- Database backup/restore procedures (future work)
- Database replication or clustering (future work)
- Performance optimization beyond basic indexes (future work)

## Decisions

### Decision: Use Alembic Autogenerate for Initial Migration
**Rationale**: Alembic's autogenerate feature can detect all SQLAlchemy models and create the migration automatically. This reduces manual work and ensures consistency with the model definitions.

**Alternatives Considered**:
- Manual migration creation: More error-prone and time-consuming
- Raw SQL scripts: Bypasses Alembic and makes future migrations harder

### Decision: Import All Models in env.py
**Rationale**: Alembic needs to import all models to detect them during autogenerate. The env.py already imports models, but we need to verify all are included.

**Implementation**: Ensure `User`, `ApiKey`, `Budget`, `Policy`, `Payment`, `APIRequest` are all imported in `backend/database/migrations/env.py`.

### Decision: Use PostgreSQL Native Enums
**Rationale**: SQLAlchemy Enum types with `native_enum=True` create PostgreSQL ENUM types, which are more efficient and type-safe than VARCHAR with CHECK constraints.

**Implementation**: Models already use `Enum` types. Alembic will create PostgreSQL ENUM types automatically.

### Decision: Foreign Key Constraints with ON DELETE Behavior
**Rationale**: Foreign keys ensure referential integrity. We need to decide on cascade behavior:
- `api_keys.user_id` → `users.user_id`: CASCADE DELETE (if user deleted, delete their API keys)
- `budgets.user_id` → `users.user_id`: CASCADE DELETE (if user deleted, delete their budgets)
- `policies.user_id` → `users.user_id`: CASCADE DELETE (if user deleted, delete their policies)
- `payments.user_id` → `users.user_id`: RESTRICT DELETE (preserve payment history even if user deleted)
- `requests.user_id` → `users.user_id`: RESTRICT DELETE (preserve request history)

**Implementation**: SQLAlchemy ForeignKey with `ondelete` parameter. Default is RESTRICT, but we may want CASCADE for some relationships.

## Risks / Trade-offs

### Risk: Migration Fails Due to Missing Dependencies
**Mitigation**: Verify all models can be imported before running autogenerate. Check for circular imports.

### Risk: Enum Types Not Created Properly
**Mitigation**: Test migration on a fresh database. Verify enum types exist in PostgreSQL after migration.

### Risk: Foreign Key Constraints Too Restrictive
**Mitigation**: Review cascade behavior. Can be adjusted in future migrations if needed.

### Risk: Missing Indexes
**Mitigation**: Models already define indexes (e.g., `__table_args__` in ApiKey). Verify autogenerate includes them.

## Migration Plan

1. **Verify Prerequisites**:
   - PostgreSQL database is running and accessible
   - `DATABASE_URL` environment variable is set
   - All models can be imported without errors

2. **Create Initial Migration**:
   - Run `alembic revision --autogenerate -m "Initial migration"`
   - Review generated migration file
   - Verify all tables, columns, indexes, and foreign keys are included

3. **Apply Migration**:
   - Run `alembic upgrade head`
   - Verify tables are created in database
   - Verify enum types exist
   - Verify indexes are created

4. **Validation**:
   - Connect to database and verify schema
   - Check foreign key relationships
   - Verify indexes exist

## Open Questions
- Should we add any additional indexes beyond what's in the models? (Answer: No, keep it minimal for now)
- Should we add database constraints beyond foreign keys? (Answer: No, models already define what's needed)
- Should we create a seed script for initial data? (Answer: No, separate concern)

