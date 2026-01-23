# Backend Architecture Restructure - Design Document

## Context

The SmartSpace backend currently has a minimal structure with:
- Single Flask app (`app.py`) with basic routes
- Chatbot service in `src/chatbot.py`
- Agentic brain system in `agentic/` directory (separate package)
- No clear separation of concerns
- No database layer
- No service abstraction
- Difficult to extend with new features

The backend needs to support:
- User and project management
- Budget tracking and spending
- Policy management
- Payment processing (Arc blockchain + USDC)
- Provider API gateway
- Audit logging
- Integration with agentic brain
- Chatbot service
- Future features (analytics, notifications, etc.)

## Goals / Non-Goals

### Goals
- Create a scalable, modular architecture that's easy to extend
- Follow Python best practices and design patterns
- Enable easy testing with dependency injection
- Support multiple API versions
- Maintain clear separation of concerns
- Integrate seamlessly with agentic brain
- Support both RESTful APIs and future GraphQL if needed
- Enable horizontal scaling

### Non-Goals
- Complete rewrite of agentic brain (it's already well-structured)
- Migration of existing data (no production data yet)
- Implementation of all services (focus on structure first)
- Frontend changes
- Database technology choice (abstracted through repository pattern)

## Decisions

### Decision 1: Layered Architecture Pattern
**What**: Use a layered architecture with clear boundaries:
- **Routes Layer**: HTTP routing and request/response handling
- **Controllers Layer**: Request validation and orchestration
- **Services Layer**: Business logic and domain operations
- **Repositories Layer**: Data access and persistence
- **Models Layer**: Data models and schemas

**Why**: 
- Clear separation of concerns
- Easy to test each layer independently
- Follows common Python web framework patterns
- Makes it easy to swap implementations (e.g., database)

**Alternatives considered**:
- Hexagonal architecture: Too complex for current needs
- MVC: Less clear separation for API-focused backend
- Microservices: Overkill for current scale

### Decision 2: Service-Oriented Structure
**What**: Organize business logic into service modules:
- `services/users/` - User management
- `services/budgets/` - Budget tracking
- `services/policies/` - Policy management
- `services/payments/` - Payment processing
- `services/providers/` - Provider API gateway
- `services/audit/` - Audit logging
- `services/agentic/` - Agentic brain integration
- `services/chatbot/` - Chatbot service

**Why**:
- Each service has single responsibility
- Easy to add new services
- Services can be tested independently
- Clear boundaries for future microservice split if needed

**Alternatives considered**:
- Monolithic service class: Hard to maintain and test
- Domain-driven design: Too complex for current needs

### Decision 3: Repository Pattern for Data Access
**What**: Abstract data access behind repository interfaces:
- `repositories/users/` - User data access
- `repositories/budgets/` - Budget data access
- `repositories/policies/` - Policy data access
- etc.

**Why**:
- Easy to swap database implementations
- Testable with mock repositories
- Clear data access boundaries
- Supports future database migrations

**Alternatives considered**:
- Direct ORM usage: Tight coupling to database
- Active Record pattern: Less flexible

### Decision 4: Dependency Injection Container
**What**: Use a simple dependency injection pattern:
- Service instances created at application startup
- Dependencies injected through constructors
- Container manages service lifecycle

**Why**:
- Easy to test with mocks
- Clear dependency graph
- Supports configuration-based service selection
- Common pattern in modern Python apps

**Alternatives considered**:
- Global singletons: Hard to test
- Factory pattern: More boilerplate

### Decision 5: API Versioning Strategy
**What**: Use URL-based versioning (`/api/v1/`, `/api/v2/`)
- Version in route path
- Separate route modules per version
- Shared services and models

**Why**:
- Clear version boundaries
- Easy to maintain multiple versions
- Standard RESTful approach
- Frontend can target specific versions

**Alternatives considered**:
- Header-based versioning: Less discoverable
- Query parameter versioning: Clutters URLs

### Decision 6: Agentic Brain Integration
**What**: Integrate agentic brain as a service:
- Import agentic brain as Python module
- Wrap in service layer for error handling and logging
- Use dependency injection for agentic brain instance
- Maintain agentic brain's READ-ONLY principle

**Why**:
- Keeps agentic brain decoupled
- Easy to test with mock agentic brain
- Clear integration point
- Maintains separation of concerns

**Alternatives considered**:
- HTTP API to agentic brain: Unnecessary overhead
- Direct imports everywhere: Tight coupling

### Decision 7: Configuration Management
**What**: Centralized configuration:
- Environment-based config files
- Configuration classes per environment
- Secrets management via environment variables
- Config validation on startup

**Why**:
- Single source of truth
- Easy to manage different environments
- Secure secret handling
- Type-safe configuration

**Alternatives considered**:
- Scattered config: Hard to manage
- Database-stored config: Overhead for simple values

## Architecture Structure

```
backend/
├── app.py                    # Flask app factory
├── config/
│   ├── __init__.py
│   ├── settings.py           # Configuration classes
│   └── development.py        # Dev-specific config
├── src/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── budgets.py
│   │   │   ├── policies.py
│   │   │   ├── payments.py
│   │   │   ├── requests.py
│   │   │   ├── providers.py
│   │   │   ├── audit.py
│   │   │   └── chatbot.py
│   │   └── health.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── users_controller.py
│   │   ├── budgets_controller.py
│   │   ├── policies_controller.py
│   │   ├── payments_controller.py
│   │   ├── requests_controller.py
│   │   ├── providers_controller.py
│   │   ├── audit_controller.py
│   │   └── chatbot_controller.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   └── user_service.py
│   │   ├── budgets/
│   │   │   ├── __init__.py
│   │   │   └── budget_service.py
│   │   ├── policies/
│   │   │   ├── __init__.py
│   │   │   └── policy_service.py
│   │   ├── payments/
│   │   │   ├── __init__.py
│   │   │   └── payment_service.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   └── provider_service.py
│   │   ├── audit/
│   │   │   ├── __init__.py
│   │   │   └── audit_service.py
│   │   ├── agentic/
│   │   │   ├── __init__.py
│   │   │   └── agentic_service.py
│   │   └── chatbot/
│   │       ├── __init__.py
│   │       └── chatbot_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py           # Base repository interface
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   └── user_repository.py
│   │   ├── budgets/
│   │   │   ├── __init__.py
│   │   │   └── budget_repository.py
│   │   ├── policies/
│   │   │   ├── __init__.py
│   │   │   └── policy_repository.py
│   │   └── ...
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── budget.py
│   │   ├── policy.py
│   │   ├── payment.py
│   │   ├── request.py
│   │   └── ...
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── error_handler.py
│   │   ├── request_validator.py
│   │   └── logging.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── responses.py
│   │   ├── exceptions.py
│   │   └── validators.py
│   └── container.py          # Dependency injection container
├── database/
│   ├── __init__.py
│   ├── migrations/           # Database migrations
│   └── schema.sql            # Initial schema (if using SQL)
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── services/
│   │   ├── controllers/
│   │   └── repositories/
│   ├── integration/
│   │   ├── api/
│   │   └── services/
│   └── fixtures/
├── agentic/                  # Existing agentic brain (unchanged)
└── requirements.txt
```

## Risks / Trade-offs

### Risk 1: Over-engineering
**Risk**: Creating too much abstraction for current needs
**Mitigation**: Start with minimal viable structure, add complexity only when needed

### Risk 2: Breaking Changes
**Risk**: Restructuring may break existing integrations
**Mitigation**: 
- No production data exists yet
- Maintain backward compatibility for chatbot endpoint during transition
- Use feature flags for gradual rollout

### Risk 3: Learning Curve
**Risk**: Team needs to learn new structure
**Mitigation**:
- Clear documentation
- Code examples
- Pair programming during initial implementation

### Risk 4: Performance Overhead
**Risk**: Additional layers may add latency
**Mitigation**:
- Profile critical paths
- Use async/await where appropriate
- Cache frequently accessed data

## Migration Plan

### Phase 1: Foundation (Week 1)
1. Create new directory structure
2. Set up configuration management
3. Create dependency injection container
4. Implement base repository and service patterns
5. Add middleware (error handling, logging)

### Phase 2: Core Services (Week 2)
1. Migrate chatbot service to new structure
2. Create user service and repository
3. Create budget service and repository
4. Create policy service and repository
5. Add database layer (choose DB technology)

### Phase 3: Integration (Week 3)
1. Integrate agentic brain as service
2. Create payment service
3. Create provider gateway service
4. Create audit service
5. Create request processing service

### Phase 4: API Layer (Week 4)
1. Create route handlers
2. Create controllers
3. Add request validation
4. Add authentication middleware
5. Add API versioning

### Phase 5: Testing & Documentation (Week 5)
1. Write unit tests for services
2. Write integration tests for APIs
3. Update documentation
4. Performance testing
5. Code review and refinement

## Open Questions

1. **Database Technology**: SQL (PostgreSQL) vs NoSQL (MongoDB)? 
   - Recommendation: Start with PostgreSQL for ACID guarantees and relational data
   
2. **ORM vs Raw SQL**: Use SQLAlchemy ORM or raw SQL?
   - Recommendation: SQLAlchemy for productivity, raw SQL for complex queries
   
3. **Caching Strategy**: Redis for caching?
   - Recommendation: Add Redis later when needed for performance
   
4. **Message Queue**: Need async task processing?
   - Recommendation: Add Celery/RQ later if needed for background jobs
   
5. **API Documentation**: OpenAPI/Swagger?
   - Recommendation: Yes, use Flask-RESTX or similar for auto-generated docs

