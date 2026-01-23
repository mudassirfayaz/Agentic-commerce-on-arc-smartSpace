# Backend

Backend API and server logic for SmartSpace platform.

## Architecture

The backend follows a layered architecture pattern with clear separation of concerns:

- **Routes Layer**: HTTP routing and request/response handling (`src/routes/`)
- **Controllers Layer**: Request validation and orchestration (`src/controllers/`)
- **Services Layer**: Business logic and domain operations (`src/services/`)
- **Repositories Layer**: Data access and persistence (`src/repositories/`)
- **Models Layer**: Data models and schemas (`src/models/`) - SQLAlchemy ORM
- **Middleware**: Cross-cutting concerns (auth, error handling, logging) (`src/middleware/`)
- **Utils**: Utility functions (responses, validators, exceptions) (`src/utils/`)

## Responsibilities

- Platform logic and API gateway
- User and project management
- Payment processing integration
- Security and authentication
- Usage tracking and logging
- API request handling and routing
- Agentic brain integration
- Chatbot service

## Status

✅ **Restructured** - New modular architecture implemented with FastAPI and PostgreSQL. Core structure in place, services and repositories ready for implementation.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.10+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Package Manager**: pip (requirements.txt)
- **Architecture**: Layered architecture with dependency injection

## Getting Started

1. Navigate to this directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
   - Create a PostgreSQL database
   - Set `DATABASE_URL` environment variable:
     ```bash
     export DATABASE_URL="postgresql://user:password@localhost:5432/smartspace"
     ```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Configure environment variables (see Environment Variables section)

6. Run the development server:
```bash
python app.py
```

Or with uvicorn directly:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 5000
```

## Folder Structure

```
backend/
├── app.py                    # FastAPI app factory
├── alembic.ini               # Alembic configuration
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration classes
├── src/
│   ├── database/             # Database configuration
│   │   ├── base.py          # SQLAlchemy base and session
│   │   └── session.py       # Session factory
│   ├── routes/
│   │   ├── v1/               # API v1 routes
│   │   └── health.py          # Health check routes
│   ├── controllers/          # Request orchestration
│   ├── services/              # Business logic
│   │   ├── users/
│   │   ├── budgets/
│   │   ├── policies/
│   │   ├── payments/
│   │   ├── providers/
│   │   ├── audit/
│   │   ├── agentic/           # Agentic brain integration
│   │   └── chatbot/           # Chatbot service
│   ├── repositories/          # Data access
│   │   ├── base.py            # Base repository interface
│   │   ├── users/
│   │   ├── budgets/
│   │   ├── policies/
│   │   ├── payments/
│   │   └── audit/
│   ├── models/                # SQLAlchemy ORM models
│   ├── middleware/            # Cross-cutting concerns
│   ├── utils/                 # Utilities
│   └── container.py           # Dependency injection
├── database/
│   └── migrations/           # Alembic migrations
│       ├── env.py             # Alembic environment
│       ├── script.py.mako     # Migration template
│       └── versions/          # Migration files
├── tests/                     # Test suite
│   ├── unit/
│   └── integration/
└── agentic/                   # Agentic brain (existing)
```

## Environment Variables

- `ENVIRONMENT`: Environment name (development, production, test)
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: PostgreSQL connection URL (e.g., `postgresql://user:password@localhost:5432/smartspace`)
- `GEMINI_API_KEY`: Gemini API key for chatbot
- `SMARTSPACE_DOC_PATH`: Path to SmartSpace.md documentation
- `ARC_TESTNET_RPC_URL`: Arc testnet RPC endpoint
- `USDC_CONTRACT_ADDRESS`: USDC contract address
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins

## Database Setup

### Initial Migration

Create the initial migration:
```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply migrations:
```bash
alembic upgrade head
```

### Database Models

All models are defined in `src/models/` using SQLAlchemy ORM:
- `User` - User accounts
- `Budget` - Budget tracking
- `Policy` - Policy configuration
- `Payment` - Payment records
- `APIRequest` - API request records

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Chatbot (v1)
- `POST /api/v1/chatbot/chat` - Chatbot chat endpoint

### API Documentation
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

### Future Endpoints
- User management endpoints
- Budget management endpoints
- Policy management endpoints
- Payment processing endpoints
- Request processing endpoints
- Provider gateway endpoints
- Audit log endpoints

## Service Architecture

### Services
Each service encapsulates business logic for a specific domain:
- **UserService**: User management operations
- **BudgetService**: Budget tracking and management
- **PolicyService**: Policy management
- **PaymentService**: Payment processing
- **ProviderService**: Provider API gateway
- **AuditService**: Audit logging
- **AgenticService**: Agentic brain integration
- **ChatbotService**: Chatbot functionality

### Repositories
Repositories abstract data access using SQLAlchemy:
- **UserRepository**: User data access
- **BudgetRepository**: Budget data access
- **PolicyRepository**: Policy data access
- **PaymentRepository**: Payment data access
- **AuditRepository**: Audit data access

### Dependency Injection
Services are registered in the container and dependencies are injected through constructors, enabling easy testing and configuration.

## Development

### Adding a New Service

1. Create service directory: `src/services/<service_name>/`
2. Create service class: `src/services/<service_name>/<service_name>_service.py`
3. Create repository if needed: `src/repositories/<service_name>/`
4. Create SQLAlchemy model: `src/models/<service_name>.py`
5. Register service in container: `app.py`
6. Create controller: `src/controllers/<service_name>_controller.py`
7. Create routes: `src/routes/v1/<service_name>.py`
8. Register routes in app: `app.py`

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

### Testing

Tests are organized by type:
- **Unit tests**: `tests/unit/` - Test individual components
- **Integration tests**: `tests/integration/` - Test complete flows

Run tests:
```bash
pytest tests/
```

## FastAPI Features

- **Automatic API Documentation**: Swagger UI at `/docs` and ReDoc at `/redoc`
- **Request Validation**: Automatic validation using Pydantic models
- **Type Safety**: Full type hints support
- **Async Support**: Native async/await support
- **Dependency Injection**: Built-in dependency injection system

## Notes

- The architecture is designed to be scalable and easy to extend
- Services can be tested independently with mocked dependencies
- Database implementation uses SQLAlchemy ORM with PostgreSQL
- API versioning is supported through URL-based versioning (`/api/v1/`, `/api/v2/`)
- All models use SQLAlchemy ORM for database operations
- Alembic is used for database migrations
