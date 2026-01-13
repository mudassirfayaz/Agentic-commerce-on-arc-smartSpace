# SmartSpace Agentic Commerce Flow

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND / USER                          │
│  - User makes API request                                       │
│  - Agent via platform link submits request                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 1. Submit request
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND API                               │
│  - Receives request from frontend (HTTP endpoint)               │
│  - Validates basic auth/session                                 │
│  - Calls Agentic Brain (Python import)                          │
│                                                                 │
│  Backend implements HTTP layer with:                            │
│  - FastAPI / Flask / Express / etc.                             │
│  - Their own routing and validation                             │
│  - Import: from agentic.src.main import AgenticBrain           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 2. brain.process_request()
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AGENTIC BRAIN (This Package)                  │
│                                                                 │
│  Step 1: Create Audit Log                                      │
│  ├─ Initialize tracking                                        │
│  └─ Log request source (user/agent)                            │
│                                                                 │
│  Step 2: Validate User                                         │
│  ├─ Fetch user context from backend                            │
│  ├─ Check account status (active/suspended)                    │
│  ├─ Verify account verification                                │
│  └─ Validate user can make requests                            │
│                                                                 │
│  Step 3: Create Request Object                                 │
│  └─ Build APIRequest with all parameters                       │
│                                                                 │
│  Step 4: Fetch Policies                                        │
│  ├─ Fetch SYSTEM policy (platform-wide rules)                  │
│  └─ Fetch USER policy (user preferences)                       │
│                                                                 │
│  Step 5: Check Compliance                                      │
│  ├─ Check system policy (blocked providers/models)             │
│  ├─ Check user policy (whitelisted providers/models)           │
│  ├─ Validate rate limits                                       │
│  └─ REJECT if violations found                                 │
│                                                                 │
│  Step 6: Estimate Cost                                         │
│  ├─ Get provider pricing                                       │
│  ├─ Calculate based on tokens                                  │
│  └─ Detect cost anomalies                                      │
│                                                                 │
│  Step 7: Check Budget                                          │
│  ├─ Check per-request limit                                    │
│  ├─ Check daily budget                                         │
│  ├─ Check monthly budget                                       │
│  └─ REJECT if insufficient budget                              │
│                                                                 │
│  Step 8: Assess Risk                                           │
│  ├─ Fetch user baseline (30-day history)                       │
│  ├─ Detect anomalies:                                          │
│  │   ├─ Cost spike (>3x average)                               │
│  │   ├─ Rate spike (unusual volume)                            │
│  │   ├─ Unusual provider                                       │
│  │   ├─ Unusual model                                          │
│  │   ├─ Unusual time pattern                                   │
│  │   ├─ New/unknown agent                                      │
│  │   ├─ Repeated rejections                                    │
│  │   └─ Budget exhaustion pattern                              │
│  ├─ Calculate risk score (1-10)                                │
│  └─ Generate recommendation (approve/review/reject)            │
│                                                                 │
│  Step 9: Make Decision                                         │
│  ├─ Check risk score vs threshold                              │
│  ├─ Check recommendation                                       │
│  ├─ Determine outcome:                                         │
│  │   ├─ APPROVED (risk ≤ threshold, all checks pass)           │
│  │   ├─ REQUIRES_REVIEW (high risk but not critical)           │
│  │   └─ REJECTED (policy violation, budget, or critical risk)  │
│  └─ Create Decision object                                     │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ If APPROVED
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROVIDER APIs                                │
│  - OpenAI (GPT-4, GPT-3.5, GPT-4o)                             │
│  - Anthropic (Claude 3 Opus, Sonnet, Haiku)                    │
│  - Google, Cohere, etc.                                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 3. API Response
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AGENTIC BRAIN (Process Response)              │
│                                                                 │
│  Step 10: Process Provider Response                            │
│  ├─ Extract actual tokens used                                 │
│  ├─ Calculate actual cost                                      │
│  ├─ Store response data                                        │
│  └─ Finalize audit log                                         │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 4. Return result + state updates
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND API                               │
│                                                                 │
│  Receives from Brain:                                           │
│  ├─ Decision (approved/rejected)                               │
│  ├─ Request details                                            │
│  ├─ Execution results (if approved)                            │
│  ├─ Actual cost and tokens                                     │
│  └─ Complete audit log                                         │
│                                                                 │
│  Backend Actions:                                               │
│  ├─ Update database with request                               │
│  ├─ Update user spending                                       │
│  ├─ Update budget tracking                                     │
│  ├─ Store audit trail                                          │
│  ├─ Update usage statistics                                    │
│  └─ Persist all state                                          │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ 5. Final response
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FRONTEND / USER                           │
│  - Display API response                                         │
│  - Show cost information                                        │
│  - Display any errors/rejections                               │
│  - Update UI state                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Separation of Concerns

### Frontend Responsibilities
- User interface and interaction
- Collect request parameters
- Display results
- Handle user authentication (session)

### Backend Responsibilities
- **Implement HTTP layer** (FastAPI, Flask, Express, etc.)
- Receive requests from frontend via HTTP endpoints
- Basic authentication/authorization
- **Import and call** Agentic Brain (Python function call)
- Receive results from Brain
- **Persist all state to database**
- Update spending/usage/budgets
- Store audit trails
- Return final response to frontend

### Agentic Brain Responsibilities (This Package)
- **READ-ONLY** operations for context
- Validate user eligibility
- Enforce policies (system + user)
- Estimate and validate costs
- Check budget availability
- Assess risk and detect anomalies
- Make intelligent decisions
- **Execute provider API calls**
- Return results for backend to persist

## Data Flow Example

```
1. User submits: "Summarize this text" → Frontend
2. Frontend → Backend: POST /api/requests (Backend's HTTP endpoint)
3. Backend → Brain: brain.process_request(params) (Direct Python call)
4. Brain validates user ✓/api/v1/process {user, params}
4. Brain validates user ✓
5. Brain checks policies ✓
6. Brain estimates cost: $0.015 ✓
7. Brain checks budget: Available ✓
8. Brain assesses risk: 2.5/10 (low) ✓
9. Brain decides: APPROVED ✓
10. Brain → OpenAI: Call GPT-4
11. OpenAI → Brain: Response + actual cost $0.016
12. Brain → Backend: {success, response, cost, decision, audit}
13. Backend updates database
14. Backend → Frontend: {success, data, cost}
15. Frontend displays result to user
```

### Rejected Request (Policy Violation)
```
1. User submits: Request with blocked provider → Frontend
2. Frontend → Backend: POST /api/requests (Backend's HTTP endpoint)
3. Backend → Brain: brain.process_request(params) (Direct Python call)
4. Brain validates user ✓
5. Brain checks policies ✗ (provider blocked in system policy)
6. Brain decides: REJECTED (policy violation)
7. Brain → Backend: {success: false, decision: rejected, reason}
8. Backend updates database (rejected request)
9. Backend → Frontend: {success: false, reason}
10. Frontend displays error to user
```

### High Risk Request (Requires Review)
```
1. Agent submits: Large cost request → Frontend
2. Frontend → Backend: POST /api/requests (Backend's HTTP endpoint)
3. Backend → Brain: brain.process_request(params) (Direct Python call)
4. Brain validates user ✓
5. Brain checks policies ✓
6. Brain estimates cost: $50.00 ✓
7. Brain checks budget: Available ✓
8. Brain assesses risk: 8.5/10 (high - cost spike, new agent)
9. Brain decides: REQUIRES_REVIEW
10. Brain → Backend: {success: false, decision: review, risk_factors}
11. Backend flags for human review
12. Backend → Frontend: {requires_review: true, reason}
13. Frontend displays "Pending Review" to user
```
