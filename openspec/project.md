# Project Context

## Purpose

**SmartSpace** is an autonomous pay-per-use API access gateway with USDC payments on the Arc blockchain. It enables secure API usage for AI agents and applications without exposing API keys, providing controlled, transparent, and predictable billing.

### Core Value Proposition
- **No API Key Exposure**: Users never need to manage or expose API keys
- **Pay-Per-Use**: Single USDC transaction per request (no subscriptions)
- **Unified Access**: One API key for all models - just change endpoint/company name
- **No Middleman Charges**: Direct pay-as-you-go, no hidden fees
- **Model Flexibility**: Easy switching between models (Qalb, DeepSeek, LLaMA, etc.) via dropdown
- **Autonomous Decision Making**: AI agents can safely make paid API calls with automatic approval/rejection
- **Complete Control**: Provider/model whitelisting, budget limits, risk assessment
- **Full Transparency**: Immutable audit trail for every request and payment
- **AI-Powered Guidance**: Gemini chatbot on landing page and web application to guide users based on SmartSpace.md documentation

### Problem Solved
- Shared API keys are risky and hard to manage
- Monthly billing is unpredictable
- Hard to track exact usage per request
- Difficult for finance teams to audit
- AI agents cannot safely make paid API calls autonomously

### Target Users
- AI startups and enterprise AI teams
- Agent-based systems requiring autonomous API access
- SaaS platforms using AI APIs
- Developers wanting safe, controlled API usage

## Tech Stack

### Frontend (`frontend/`)
- **Framework**: React 18.2.0
- **Routing**: React Router DOM 6.20.0
- **Build Tool**: Vite 5.0.8
- **Styling**: CSS (component-scoped CSS files)
- **Language**: JavaScript (JSX)

**Key Dependencies**:
- `react`, `react-dom`, `react-router-dom`
- `@vitejs/plugin-react` for Vite integration

### Backend (`backend/`)
- **Status**: In development
- **Responsibilities**: HTTP layer, database persistence, state management
- **Integration**: Imports and calls Agentic Brain as Python module
- **Expected Stack**: FastAPI/Flask/Express (to be determined)

### Agentic System (`infra/agentic/`)
- **Language**: Python 3.10+
- **Package Manager**: UV (pyproject.toml)
- **Testing**: pytest 9.0.2+ with pytest-asyncio
- **Key Dependencies**:
  - `requests>=2.32.0` for HTTP client
  - `python-dotenv>=1.2.1` for environment configuration
  - `pytest>=9.0.2`, `pytest-asyncio>=1.3.0`, `pytest-cov>=7.0.0` for testing

## Project Conventions

### Code Style

#### Python (Agentic System)
- **Format**: Follow PEP 8 conventions
- **Type Hints**: Use type hints for function parameters and return types
- **Async/Await**: Use `async`/`await` for all I/O operations
- **Dataclasses**: Use `@dataclass` for model definitions (see `models/`)
- **Logging**: Use Python `logging` module with structured log messages
- **Error Handling**: Use specific exceptions, log errors with context
- **Naming**:
  - Classes: `PascalCase` (e.g., `AgenticBrain`, `UserContext`)
  - Functions/methods: `snake_case` (e.g., `process_request`, `fetch_from_backend`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `BACKEND_API_URL`)
  - Private methods: prefix with `_` (e.g., `_create_request_from_data`)

#### JavaScript/React (Frontend)
- **Format**: Standard JavaScript/JSX
- **Components**: Functional components with hooks
- **File Structure**: One component per file, co-located CSS files
- **Naming**:
  - Components: `PascalCase` (e.g., `Dashboard`, `ApiCallInterface`)
  - Files: Match component name (e.g., `Dashboard.jsx`, `Dashboard.css`)
  - Functions: `camelCase` (e.g., `handleSubmit`, `fetchData`)
  - CSS classes: `kebab-case` (e.g., `dashboard-container`, `stats-cards`)

### Frontend Design System

**⚠️ CRITICAL: Apply these guidelines when creating or updating ANY frontend component.**

You are a senior React engineer with 15+ years of production experience and strong UI/UX judgment.

#### Color System

Apply the following color system consistently and intentionally across the entire frontend:

- **`#080808`** → Primary background (app shell, main layout)
- **`#212121`** → Secondary background (cards, panels, sections)
- **`#F2F2F2`** → Primary text, icons, and high-contrast UI elements
- **`#BB4EEF`** → Accent color (CTAs, active states, focus rings, highlights only)

#### Design Rules (Must Be Followed Strictly)

**Overall Aesthetic:**
- Use a dark, premium, minimal aesthetic. No visual noise.
- The UI should feel enterprise-grade, timeless, and emotionally confident
- Every element should look deliberate, polished, and production-ready

**Cards:**
- Subtle elevation, soft shadows, no harsh borders
- Consistent padding and spacing
- Rounded corners (balanced, not exaggerated)

**Icons:**
- Monochrome by default using `#F2F2F2`
- Use `#BB4EEF` only for active, selected, or primary actions
- Proper alignment and visual weight relative to text

**Typography:**
- High readability and hierarchy
- Clear distinction between headings, body, and metadata

**States:**
- Hover, focus, active, disabled states must be visually clear
- Disabled elements should feel intentional, not broken

**Accessibility:**
- Maintain strong contrast ratios
- Keyboard and focus visibility must be obvious and elegant

**Consistency:**
- No unused components
- No placeholder UI
- No broken or incomplete interactions

#### Quality Assurance

**After implementation, audit the entire frontend and fix:**
- Any visual inconsistency
- Any alignment issue
- Any contrast problem
- Any UX flaw

**Continue until the interface feels flawless and professional.**

### Architecture Patterns

#### Three-Layer Architecture

**1. Frontend Layer** (`frontend/`)
- **Responsibility**: User interface, request collection, result display
- **Pattern**: Component-based React architecture
- **Structure**:
  ```
  src/
    ├── pages/          # Route-level components
    ├── components/    # Reusable UI components
    │   └── Dashboard/ # Dashboard-specific components
    ├── App.jsx        # Root component with routing
    └── main.jsx       # Entry point
  ```
- **Key Pages**:
  - `LandingPage.jsx` - Public landing page (includes Gemini chatbot)
  - `Login.jsx`, `Signup.jsx` - Authentication
  - `Dashboard.jsx` - Main dashboard (includes Gemini chatbot)
  - `Projects.jsx`, `Agents.jsx` - Project/agent management
  - `Usage.jsx`, `Billing.jsx` - Analytics and billing
- **Chatbot Component**:
  - Gemini-powered chatbot available on landing page and throughout web application
  - **Knowledge Base**: SmartSpace.md serves as the starting point and primary context for the chatbot
  - Chatbot loads SmartSpace.md content as context for all user queries
  - Provides user guidance based on SmartSpace.md documentation
  - Helps users understand features, usage, and best practices

**2. Backend Layer** (`backend/`)
- **Responsibility**: HTTP layer, database persistence, state management
- **Pattern**: RESTful API with direct Python import of Agentic Brain
- **Key Responsibilities**:
  - Receive HTTP requests from frontend
  - Basic authentication/authorization
  - Import and call `AgenticBrain.process_request()`
  - Persist all state to database
  - Update spending/usage/budgets
  - Store audit trails
  - Return final response to frontend
- **Integration Pattern**:
  ```python
  from agentic.src.main import AgenticBrain
  
  brain = AgenticBrain()
  result = await brain.process_request(request_data)
  ```

**3. Agentic Brain Layer** (`infra/agentic/`)
- **Responsibility**: Decision making, policy enforcement, risk assessment, API execution
- **Pattern**: READ-ONLY operations, stateless processing
- **Key Principle**: Brain fetches from backend, never saves directly
- **Structure**:
  ```
  src/
    ├── main.py                    # Main orchestrator (AgenticBrain)
    ├── decision_engine/           # 12-step decision pipeline
    ├── models/                    # Data models (dataclasses)
    ├── policies/                  # Policy management
    ├── budgets/                   # Budget tracking
    ├── pricing/                   # Cost estimation
    ├── risk/                      # Risk assessment
    ├── payments/                  # Payment execution
    ├── providers/                 # Provider adapters (OpenAI, Anthropic)
    ├── integrations/              # Backend client interface
    └── audit_logging/            # Audit trail
  ```

#### Request Flow Pattern

```
1. User/Agent → Frontend: Submit request
2. Frontend → Backend: POST /api/requests (HTTP)
3. Backend → Brain: brain.process_request(params) (Python call)
4. Brain Processing (12 steps):
   a. Validate request structure
   b. Load user context & policies
   c. Validate provider/model whitelist
   d. Estimate costs
   e. Check budget availability
   f. Validate against policies
   g. Assess risk (anomaly detection)
   h. Route to agent tier (Flash vs Pro)
   i. Get AI decision
   j. Log everything
5. If APPROVED:
   a. Pay estimated amount (blockchain TX)
   b. Call provider API
   c. Log cost variance
6. Brain → Backend: Return response + state updates
7. Backend → Database: Persist state
8. Backend → Frontend: Return final response
9. Frontend → User: Display result
```

#### Separation of Concerns

- **Frontend**: UI/UX only, no business logic
- **Backend**: HTTP layer + persistence, no decision logic
- **Agentic Brain**: Decision logic + execution, no persistence

### Testing Strategy

#### Python (Agentic System)
- **Framework**: pytest with pytest-asyncio
- **Configuration**: `pytest.ini` with markers for test categorization
- **Test Structure**:
  ```
  tests/
    ├── test_audit_logger.py
    ├── test_backend_client.py
    └── ... (more test files)
  ```
- **Test Markers**:
  - `@pytest.mark.unit` - Unit tests for individual components
  - `@pytest.mark.integration` - Integration tests between components
  - `@pytest.mark.slow` - Tests that take longer to run
  - `@pytest.mark.models`, `@pytest.mark.policies`, etc. - Category markers
- **Coverage**: Minimum 70% coverage required (configured in pytest.ini)
- **Async Testing**: Use `asyncio_mode = auto` for async test support
- **Running Tests**:
  ```bash
  cd infra/agentic
  pytest                    # Run all tests
  pytest -m unit           # Run unit tests only
  pytest --cov=src         # Run with coverage
  python run_tests.py      # Run comprehensive test suite
  ```

#### Frontend Testing
- **Status**: Not yet configured (to be added)
- **Recommended**: Vitest or Jest with React Testing Library

### Git Workflow

#### Repository Structure
- **Monorepo**: Single repository with multiple components
- **Structure**:
  ```
  ├── frontend/          # React frontend
  ├── backend/           # Backend API (in development)
  ├── infra/agentic/     # Python agentic brain
  ├── openspec/          # OpenSpec specifications
  └── README.md          # Project overview
  ```

#### Branching Strategy
- **Main Branch**: `main` or `master` (production-ready code)
- **Feature Branches**: `feature/description` for new features
- **Component Isolation**: Each component (frontend/backend/agentic) maintains its own structure

#### Commit Conventions
- Use clear, descriptive commit messages
- Reference component affected: `[frontend]`, `[backend]`, `[agentic]`
- Examples:
  - `[agentic] Add risk assessment for cost spikes`
  - `[frontend] Implement dashboard stats cards`
  - `[backend] Integrate payment execution endpoint`

## Domain Context

### Core Concepts

#### Users & Projects
- **User**: Account holder with wallet address for USDC payments
- **Project**: Container for agents, policies, and budgets (user can have multiple projects)
- **Agent**: Autonomous entity that can make API requests (belongs to a project)
- **User Context**: Complete user state including account status, verification, spending history, behavioral baseline

#### Policies
- **System Policy**: Platform-wide rules (cannot be overridden by users)
  - Blocked providers/models
  - Global rate limits
  - Security constraints
- **User Policy**: User-specific preferences (within system bounds)
  - Allowed providers/models (whitelist)
  - Forbidden providers/operations (blacklist)
  - Budget limits (per-request, daily, monthly)
  - Rate limits (per minute/hour/day)
  - Risk thresholds
  - Allowed spending hours/days
- **Policy Enforcement**: System policy checked first, then user policy

#### Budgets
- **Per-Request Limit**: Maximum USDC per single request (default: $10.00)
- **Daily Budget**: Maximum USDC per day (default: $100.00)
- **Monthly Budget**: Maximum USDC per month (default: $3000.00)
- **Budget Tracking**: Real-time tracking of spending at all levels
- **Budget Checking**: All three levels must pass for request approval

#### Payments
- **Currency**: USDC (USD Coin stablecoin)
- **Blockchain**: Arc blockchain
- **Payment Model**: Single transaction per request (no refunds)
- **Payment Flow**:
  1. Estimate cost before execution
  2. Reserve payment (blockchain TX)
  3. Execute API call
  4. Calculate actual cost
  5. Log variance (estimated vs actual)
- **Transaction Details**: TX hash, block number, gas costs tracked

#### Risk Assessment
- **Risk Score**: 1-10 scale (1 = low risk, 10 = critical risk)
- **Anomaly Detection**:
  - Cost spike (>3x average)
  - Rate spike (unusual volume)
  - Unusual provider/model
  - Unusual time pattern
  - New/unknown agent
  - Repeated rejections
  - Budget exhaustion pattern
- **Baseline**: 30-day history used for comparison
- **Decision Impact**:
  - Risk ≤ 3: Auto-approve (Flash Agent)
  - Risk 3-7: Review required (Pro Agent)
  - Risk > 7: Reject

#### Agent Tiers
- **Flash Agent**: Fast decisions (<100ms) for low-risk, low-cost requests
  - Max risk score: 5.0
  - Max cost: $0.01
  - Auto-approve: Yes
- **Pro Agent**: Comprehensive analysis (<1s) for higher-risk or higher-cost requests
  - Max risk score: 8.0
  - Max cost: $1.00
  - Auto-approve: No (requires review)

#### API Providers & Models
- **Supported Providers**: OpenAI, Anthropic, Google, Cohere, Ollama (local), etc.
- **Demo Providers (Hackathon)**: 
  - **Ollama** (local): Qalb (Urdu LLM), DeepSeek R1, LLaMA-2, Vision/Audio models
  - Models accessible via local Ollama instance
- **Model Selection**: Dropdown UI for users to select from available models
  - Example: "Qalb (Urdu LLM)", "DeepSeek R1", "LLaMA-2"
- **Model Whitelisting**: Users can only use approved models
- **Provider Whitelisting**: Users can only use approved providers
- **Cost Calculation**: Per-provider, per-model pricing (input/output tokens)
- **Model Switching**: Users change API endpoint/company name to switch models seamlessly

#### Request Lifecycle
1. **PENDING**: Request received
2. **VALIDATING**: Being processed by brain
3. **APPROVED**: Decision made to approve
4. **REJECTED**: Decision made to reject
5. **EXECUTING**: Payment + API call in progress
6. **EXECUTED**: Successfully completed
7. **FAILED**: Error during execution
8. **CANCELLED**: Manually cancelled

#### Audit Trail
- **Immutable Logs**: Hash-chain structure for compliance
- **Events Tracked**:
  - Request received
  - Policy checks
  - Budget checks
  - Risk assessment
  - Agent decision
  - Payment execution
  - API call results
  - Errors and failures
- **Storage**: JSONL format in `audit_logs/` directory
- **Compliance**: Full audit trail for regulatory requirements

### Key Business Rules

1. **Provider/Model Whitelisting is CRITICAL**: All requests must validate against user's allowed providers/models
2. **Budget Enforcement**: All three budget levels (per-request, daily, monthly) must pass
3. **System Policy Overrides**: System policies cannot be overridden by user policies
4. **Single Payment Transaction**: One blockchain TX per request (no refunds, variance tracked)
5. **READ-ONLY Brain**: Agentic brain never persists state, backend handles all persistence
6. **Risk-Based Routing**: Low-risk requests go to Flash Agent, high-risk to Pro Agent
7. **Anomaly Detection**: 30-day baseline used for risk assessment

## Important Constraints

### Technical Constraints

1. **Agentic Brain is READ-ONLY**
   - Brain fetches data from backend via API
   - Brain never writes to database directly
   - All state persistence handled by backend
   - Brain returns results for backend to persist

2. **Backend Must Implement HTTP Layer**
   - Backend provides RESTful API endpoints
   - Backend imports Agentic Brain as Python module
   - Backend handles authentication/authorization
   - Backend manages database connections

3. **Blockchain Payment Constraints**
   - Single transaction per request (no refunds)
   - Must track transaction hash and block number
   - Must handle gas costs
   - Must support Arc blockchain + USDC
   - Payment must complete before API call

4. **Provider API Key Security**
   - API keys stored securely (never in code)
   - Keys never exposed to frontend
   - Keys managed by backend only
   - Regular key rotation required

5. **Audit Trail Immutability**
   - Audit logs must be hash-chained
   - Logs cannot be modified after creation
   - Full compliance trail required
   - JSONL format for audit logs

### Business Constraints

1. **Budget Limits are Hard Limits**
   - Cannot exceed per-request, daily, or monthly budgets
   - No overrides without policy change
   - Budget exhaustion immediately blocks requests

2. **Policy Enforcement is Mandatory**
   - System policies cannot be bypassed
   - User policies must be within system bounds
   - Provider/model whitelist validation is critical

3. **Risk Thresholds**
   - Risk > 7: Automatic rejection
   - Risk 3-7: Requires review
   - Risk < 3: Auto-approve

4. **Payment Timing**
   - Payment must execute before API call
   - No refunds for over-estimation
   - Variance tracked for optimization

### Regulatory Constraints

1. **Audit Compliance**
   - Complete audit trail for all requests
   - Immutable logs for regulatory review
   - Financial transaction tracking

2. **Data Privacy**
   - User data must be protected
   - API request content may contain sensitive data
   - Compliance with data protection regulations

## External Dependencies

### Blockchain & Payments
- **Arc Blockchain**: Primary blockchain network for USDC transactions
- **Network**: Arc testnet (for hackathon demo)
- **USDC (Circle)**: Stablecoin for payments
- **Payment Approach (Hackathon)**:
  - Direct USDC smart contract on Arc testnet
  - No Circle REST APIs required
  - On-chain USDC transfer verification only
  - Real USDC transactions on testnet
- **Payment Gateway**: Backend must implement Arc + USDC integration
- **Transaction Requirements**:
  - Return transaction hash
  - Track block number
  - Handle confirmations
  - Track gas costs
  - Payment execution in ~500ms target

### AI Provider APIs
- **OpenAI**: GPT-4, GPT-3.5, GPT-4 Vision
- **Anthropic**: Claude 3 Opus, Sonnet, Haiku
- **Google**: Gemini Pro, Gemini Pro Vision
  - **Chatbot Integration**: Gemini API used for user guidance chatbot on landing page and web application
  - **Knowledge Base**: SmartSpace.md serves as the starting point and primary context source for the chatbot
  - Chatbot loads SmartSpace.md content as context for all queries to provide accurate, documentation-based responses
- **Cohere**: (to be integrated)
- **Ollama (Local - Hackathon Demo)**:
  - Local Ollama instance required
  - Models: `qalb-urdu`, `deepseek-r1`, `llama2` (must match `ollama list`)
  - No API keys needed (local access)
  - Direct HTTP calls to local Ollama API
- **Provider Requirements**:
  - API keys managed by backend (except Ollama)
  - Cost calculation per provider/model
  - Token usage tracking
  - Response time monitoring

### Backend Services (To Be Implemented)
- **User Service**: User account management, verification, status
- **Budget Service**: Budget tracking, spending limits
- **Policy Service**: Policy storage and retrieval
- **Pricing Service**: Provider/model cost information
- **Payment Service**: Blockchain transaction execution (Arc testnet USDC)
- **Spending Service**: Spending history and analytics
- **Audit Service**: Audit log storage and retrieval
- **Provider Gateway**: Secure API key management and routing
- **API Key Service**: Generate and manage single API key per user for unified access
- **Chatbot Service**: Gemini chatbot integration for user guidance
  - **Knowledge Base**: SmartSpace.md is the starting point and primary context source
  - Backend loads SmartSpace.md content and provides it as context to Gemini API for all user queries

### Development Tools
- **Python**: 3.10+ for agentic system
- **Node.js**: For frontend development (Vite requires Node)
- **UV**: Python package manager (replaces pip)
- **pytest**: Python testing framework
- **Vite**: Frontend build tool
- **React Router**: Frontend routing

### Environment Configuration
- **Environment Variables**:
  - `BACKEND_API_URL`: Backend API base URL
  - `API_TIMEOUT`: API request timeout (default: 30s)
  - `ENVIRONMENT`: `development`, `production`, or `test`
  - Provider API keys (stored securely, never in code)
  - `GEMINI_API_KEY`: Google Gemini API key for chatbot functionality
  - `SMARTSPACE_DOC_PATH`: Path to SmartSpace.md documentation file (required - serves as starting point and primary context for chatbot)
  - `OLLAMA_BASE_URL`: Local Ollama instance URL (default: `http://localhost:11434`)
  - `ARC_TESTNET_RPC_URL`: Arc testnet RPC endpoint for USDC transactions

## Hackathon Demo Scope

### Demo Requirements
The hackathon demo focuses on demonstrating the core value proposition with minimal complexity:

**End-to-End Flow:**
1. User creates account on SmartSpace
2. User adds USDC to account (Arc testnet)
3. Balance credited to user account
4. User receives single API key for unified access
5. User selects model from dropdown (Qalb, DeepSeek, etc.)
6. User makes API call → Payment processed (~500ms)
7. API call routed to selected model (Ollama local)
8. Response returned to user

**Key Demo Features:**
- ✅ Real USDC payments on Arc testnet (no mocks)
- ✅ Single API key for all models
- ✅ Model switching via dropdown UI
- ✅ Pay-as-you-go per request
- ✅ No middleman charges
- ✅ Unified AI access interface
- ✅ Gemini chatbot for user guidance (landing page and web application)

### Implementation Priorities

**Priority 1: USDC Payment on Arc**
- Direct USDC smart contract integration on Arc testnet
- Payment execution and verification
- Transaction hash tracking

**Priority 2: API Key Authentication**
- Generate single API key per user
- API key validation and routing
- Secure key management

**Priority 3: One Model Working**
- Ollama provider adapter implementation
- At least one model (DeepSeek or Qalb) functional
- End-to-end request/response flow

**Priority 4: Model Switch Dropdown**
- Frontend dropdown component
- Model selection UI
- Dynamic endpoint routing

**Priority 5: Clean Demo UI**
- Polished user interface
- Clear payment flow visualization
- Model selection and response display

### Demo Models (Ollama)
- **Qalb (Urdu LLM)**: `qalb-urdu`
- **DeepSeek R1**: `deepseek-r1`
- **LLaMA-2**: `llama2`
- Additional models as available

**Note**: Model names must match `ollama list` output exactly.

## Implementation Guidelines

### Adding New Features

1. **Frontend Features**
   - Create component in `frontend/src/components/` or `pages/`
   - Co-locate CSS file with component
   - Use React Router for navigation
   - Follow existing component patterns
   - **MANDATORY**: Apply Frontend Design System guidelines (see "Frontend Design System" section above)
   - **Chatbot Component**: Gemini chatbot component available on landing page and dashboard
     - SmartSpace.md serves as the starting point and primary context source
     - Backend loads SmartSpace.md content and provides it to Gemini API for all queries

2. **Backend Features**
   - Implement HTTP endpoints
   - Integrate with Agentic Brain via Python import
   - Persist state to database
   - Follow RESTful API conventions

3. **Agentic Brain Features**
   - Add models in `infra/agentic/src/models/`
   - Implement business logic in appropriate module
   - Add tests in `infra/agentic/tests/`
   - Update decision engine if affecting request flow
   - Maintain READ-ONLY principle

### Code Organization

#### Frontend Structure
```
frontend/src/
├── pages/              # Route-level pages
│   ├── Dashboard.jsx
│   ├── Projects.jsx
│   └── ...
├── components/         # Reusable components
│   └── Dashboard/      # Dashboard-specific components
│       ├── Header.jsx
│       ├── Sidebar.jsx
│       └── ...
├── App.jsx            # Root with routing
└── main.jsx           # Entry point
```

#### Agentic Structure
```
infra/agentic/src/
├── main.py            # AgenticBrain orchestrator
├── config.py          # Configuration
├── models/            # Data models (dataclasses)
├── decision_engine/   # 12-step decision pipeline
├── policies/          # Policy management
├── budgets/           # Budget tracking
├── pricing/           # Cost estimation
├── risk/              # Risk assessment
├── payments/          # Payment execution
├── providers/         # Provider adapters
├── integrations/      # Backend client interface
└── audit_logging/     # Audit trail
```

### Error Handling Patterns

#### Python (Agentic)
- Use specific exception types
- Log errors with full context
- Return structured error responses
- Example:
  ```python
  try:
      result = await process_request(data)
  except ValueError as e:
      logger.error(f"Validation error: {e}", exc_info=True)
      return {'success': False, 'error': str(e)}
  ```

#### JavaScript (Frontend)
- Use try/catch for async operations
- Display user-friendly error messages
- Log errors to console (or error tracking service)
- Example:
  ```javascript
  try {
      const result = await fetchData();
  } catch (error) {
      console.error('Error:', error);
      setError('Failed to load data');
  }
  ```

### Configuration Management

#### Python Configuration
- Use `config.py` for centralized configuration
- Environment variables via `os.getenv()`
- Environment-specific configs (Development, Production, Test)
- Endpoint configuration in `Config.ENDPOINTS`

#### Frontend Configuration
- Environment variables via Vite (`import.meta.env`)
- Configuration in `vite.config.js`
- API URLs configured per environment

### Testing Best Practices

1. **Unit Tests**: Test individual functions/components in isolation
2. **Integration Tests**: Test interactions between components
3. **Async Tests**: Use `pytest-asyncio` for async Python code
4. **Mock External Services**: Mock backend API calls in agentic tests
5. **Test Coverage**: Maintain minimum 70% coverage for Python code
6. **Test Data**: Use fixtures for common test data

### Documentation Standards

1. **Code Comments**: Document complex logic and business rules
2. **Docstrings**: Use Python docstrings for all functions/classes
3. **README Files**: Component-specific READMEs in each directory
4. **Architecture Docs**: High-level architecture in `ARCHITECTURE.md`
5. **API Documentation**: Document backend API endpoints (when implemented)

## Quick Reference

### Key File Locations
- **Frontend Entry**: `frontend/src/main.jsx`
- **Frontend Routing**: `frontend/src/App.jsx`
- **Agentic Brain**: `infra/agentic/src/main.py`
- **Agentic Config**: `infra/agentic/src/config.py`
- **Decision Engine**: `infra/agentic/src/decision_engine/decision_engine.py`
- **Models**: `infra/agentic/src/models/`
- **Architecture Doc**: `infra/agentic/ARCHITECTURE.md`

### Common Commands

#### Frontend
```bash
cd frontend
npm install          # Install dependencies
npm run dev         # Start development server
npm run build       # Build for production
```

#### Agentic
```bash
cd infra/agentic
uv sync             # Install dependencies (UV)
pytest              # Run tests
python -m src.main  # Run main module
python run_tests.py # Run comprehensive tests
```

### Key Concepts Summary
- **User**: Account holder with wallet
- **Project**: Container for agents and policies
- **Agent**: Autonomous entity making requests
- **Policy**: Rules for provider/model whitelisting and budgets
- **Budget**: Per-request, daily, monthly spending limits
- **Risk Score**: 1-10 scale for anomaly detection
- **Agent Tier**: Flash (fast) vs Pro (comprehensive)
- **Payment**: Single USDC transaction per request
- **Audit Trail**: Immutable hash-chain logs
