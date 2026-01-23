# Change: Add Database and Create Corresponding Tables

## Why
The backend has SQLAlchemy models defined (`User`, `ApiKey`, `Budget`, `Policy`, `Payment`, `APIRequest`) and Alembic is configured, but no database tables have been created yet. The database migrations directory is empty, and there is no initial migration to create the schema. Without database tables, the backend cannot persist any data, making it impossible to store users, API keys, budgets, policies, payments, or request records. This is a foundational requirement that must be completed before any backend functionality can work.

## What Changes
- Create initial Alembic migration to generate all database tables from existing SQLAlchemy models
- Ensure all models are properly imported in Alembic env.py for autogenerate to detect them
- Create tables for: `users`, `api_keys`, `budgets`, `policies`, `payments`, `requests`
- Set up proper foreign key relationships between tables
- Create indexes as defined in models (e.g., `idx_api_keys_key_hash`, `idx_api_keys_user_id`)
- Ensure PostgreSQL enum types are created for: `AccountStatus`, `UserTier`, `ApiKeyStatus`, `PaymentStatus`, `RequestStatus`
- Verify migration can be applied successfully to create the database schema
- Document database setup process in backend README

## Impact
- Affected specs: backend-database (ADDED - new capability)
- Affected code:
  - `backend/database/migrations/versions/` - New initial migration file
  - `backend/database/migrations/env.py` - May need MODIFIED to ensure all models are imported
  - `backend/src/models/__init__.py` - May need MODIFIED to ensure proper exports
  - `backend/README.md` - MODIFIED to document database setup steps
- Breaking changes: None (additive only - creates new database schema)
- Dependencies:
  - Requires PostgreSQL database to be set up and accessible
  - Requires `DATABASE_URL` environment variable to be configured
  - Requires all SQLAlchemy models to be properly defined (already done)

