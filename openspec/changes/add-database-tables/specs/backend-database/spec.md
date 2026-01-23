# backend-database Specification

## Purpose
The backend database capability provides data persistence for the SmartSpace platform using PostgreSQL with SQLAlchemy ORM and Alembic migrations. This capability ensures all application data (users, API keys, budgets, policies, payments, requests) is stored reliably and can be queried efficiently.

## ADDED Requirements

### Requirement: Database Schema Initialization
The backend SHALL have a complete database schema with all required tables, relationships, indexes, and constraints created through Alembic migrations.

#### Scenario: Initial migration creates all tables
- **WHEN** the initial Alembic migration is applied
- **THEN** all tables are created: `users`, `api_keys`, `budgets`, `policies`, `payments`, `requests`
- **AND** each table has the correct columns matching the SQLAlchemy model definitions
- **AND** primary keys and unique constraints are created

#### Scenario: Foreign key relationships are established
- **WHEN** the initial migration is applied
- **THEN** foreign key constraints are created:
  - `api_keys.user_id` references `users.user_id`
  - `budgets.user_id` references `users.user_id`
  - `policies.user_id` references `users.user_id`
- **AND** foreign key constraints enforce referential integrity

#### Scenario: Indexes are created for performance
- **WHEN** the initial migration is applied
- **THEN** indexes are created as defined in models:
  - `idx_api_keys_key_hash` on `api_keys.key_hash`
  - `idx_api_keys_user_id` on `api_keys.user_id`
  - Indexes on all primary keys and foreign keys
- **AND** indexes improve query performance for common lookups

#### Scenario: PostgreSQL enum types are created
- **WHEN** the initial migration is applied
- **THEN** PostgreSQL enum types are created:
  - `accountstatus` (active, suspended, inactive)
  - `usertier` (free, pro, enterprise)
  - `apikeystatus` (active, revoked)
  - `paymentstatus` (pending, completed, failed, cancelled)
  - `requeststatus` (pending, validating, approved, rejected, executing, executed, failed, cancelled)
- **AND** enum columns use these native PostgreSQL enum types

### Requirement: Database Migration Management
The backend SHALL use Alembic for database schema version control and migrations.

#### Scenario: Initial migration can be created
- **WHEN** running `alembic revision --autogenerate -m "Initial migration"`
- **THEN** Alembic generates a migration file that includes all model changes
- **AND** the migration file is created in `backend/database/migrations/versions/`
- **AND** all models are detected by Alembic autogenerate

#### Scenario: Migration can be applied
- **WHEN** running `alembic upgrade head`
- **THEN** the migration is applied to the database
- **AND** all tables, constraints, and indexes are created
- **AND** the migration completes without errors

#### Scenario: Alembic tracks migration state
- **WHEN** a migration is applied
- **THEN** Alembic records the migration version in the `alembic_version` table
- **AND** future migrations can detect the current schema state

### Requirement: Database Connection Configuration
The backend SHALL connect to PostgreSQL using configuration from environment variables.

#### Scenario: Database connection uses DATABASE_URL
- **WHEN** the backend application starts
- **THEN** it reads `DATABASE_URL` environment variable
- **AND** it establishes a connection to the PostgreSQL database
- **AND** connection pooling is configured according to settings

#### Scenario: Database connection fails gracefully
- **WHEN** `DATABASE_URL` is missing or invalid
- **THEN** the application logs an error
- **AND** the application fails to start with a clear error message

### Requirement: Model-to-Table Mapping
All SQLAlchemy models SHALL be correctly mapped to database tables with proper column types and constraints.

#### Scenario: User model maps to users table
- **WHEN** the User model is defined
- **THEN** it maps to the `users` table
- **AND** columns include: `user_id` (primary key), `account_status`, `tier`, `total_spending`, `available_balance`, `total_requests`, `created_at`, `last_request_at`
- **AND** enum columns use PostgreSQL enum types

#### Scenario: ApiKey model maps to api_keys table
- **WHEN** the ApiKey model is defined
- **THEN** it maps to the `api_keys` table
- **AND** columns include: `id` (primary key, autoincrement), `user_id` (foreign key), `key_hash` (unique), `created_at`, `last_used_at`, `usage_count`, `status`
- **AND** indexes are created on `key_hash` and `user_id`

#### Scenario: Budget model maps to budgets table
- **WHEN** the Budget model is defined
- **THEN** it maps to the `budgets` table
- **AND** columns include: `id` (primary key), `user_id` (foreign key), `project_id`, `daily_limit`, `monthly_limit`, `per_request_limit`, `current_daily_spending`, `current_monthly_spending`, `period_start`, `period_end`

#### Scenario: Policy model maps to policies table
- **WHEN** the Policy model is defined
- **THEN** it maps to the `policies` table
- **AND** columns include: `id` (primary key), `user_id` (foreign key), `project_id`, `allowed_providers` (JSON), `allowed_models` (JSON), `rate_limits` (JSON), `forbidden_operations` (JSON), `require_approval_above`

#### Scenario: Payment model maps to payments table
- **WHEN** the Payment model is defined
- **THEN** it maps to the `payments` table
- **AND** columns include: `payment_id` (primary key), `user_id`, `request_id`, `amount`, `currency`, `network`, `tx_hash`, `block_number`, `status`, `created_at`
- **AND** enum column `status` uses PostgreSQL enum type

#### Scenario: APIRequest model maps to requests table
- **WHEN** the APIRequest model is defined
- **THEN** it maps to the `requests` table
- **AND** columns include: `request_id` (primary key), `user_id`, `project_id`, `agent_id`, `api_provider`, `model_name`, `endpoint`, `parameters` (JSON), `status`, `estimated_cost`, `actual_cost`, `created_at`
- **AND** enum column `status` uses PostgreSQL enum type

