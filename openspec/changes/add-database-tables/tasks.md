## 1. Prerequisites and Verification
- [ ] 1.1 Verify PostgreSQL database is accessible and `DATABASE_URL` environment variable is set
- [ ] 1.2 Verify all SQLAlchemy models can be imported without errors (`User`, `ApiKey`, `Budget`, `Policy`, `Payment`, `APIRequest`)
- [ ] 1.3 Verify `backend/database/migrations/env.py` imports all models correctly
- [ ] 1.4 Test database connection from backend application

## 2. Create Initial Migration
- [ ] 2.1 Run `alembic revision --autogenerate -m "Initial migration"` to generate migration file
- [ ] 2.2 Review generated migration file in `backend/database/migrations/versions/`
- [ ] 2.3 Verify migration includes all tables: `users`, `api_keys`, `budgets`, `policies`, `payments`, `requests`
- [ ] 2.4 Verify migration includes all foreign key relationships
- [ ] 2.5 Verify migration includes all indexes (e.g., `idx_api_keys_key_hash`, `idx_api_keys_user_id`)
- [ ] 2.6 Verify migration includes PostgreSQL enum types for all Enum columns
- [ ] 2.7 Manually review and adjust migration if needed (e.g., foreign key cascade behavior)

## 3. Apply Migration and Verify
- [ ] 3.1 Run `alembic upgrade head` to apply migration
- [ ] 3.2 Verify migration completes without errors
- [ ] 3.3 Connect to PostgreSQL database and verify all tables exist
- [ ] 3.4 Verify all enum types are created in PostgreSQL (`accountstatus`, `usertier`, `apikeystatus`, `paymentstatus`, `requeststatus`)
- [ ] 3.5 Verify foreign key constraints are created correctly
- [ ] 3.6 Verify indexes are created (check `\d+ table_name` in psql or use database tool)
- [ ] 3.7 Verify table structures match model definitions (column types, nullability, defaults)

## 4. Documentation and Testing
- [ ] 4.1 Update `backend/README.md` with database setup instructions
- [ ] 4.2 Document the migration process in README
- [ ] 4.3 Add note about `DATABASE_URL` environment variable requirement
- [ ] 4.4 Test that backend can connect to database and query tables
- [ ] 4.5 Verify Alembic can detect future model changes (test by adding a dummy column, then removing it)

