# SmartSpace Agentic Brain



## 🎯 Overview

The SmartSpace Agentic Brain is an intelligent system that autonomously evaluates, approves, and pays  for AI API requests with automatic blockchain payments. It provides complete cost control, security, compliance, and auditability for pay-per-use AI services.

**Key Innovation**: No subscriptions. Pay only for actual usage via Arc blockchain + USDC stablecoin(circle).

## ✨ Key Features

- ✅ **Autonomous Decision Making**: 12-step evaluation pipeline with AI agents
- ✅ **Automatic Blockchain Payments**: Single transaction per request (Arc + USDC)
- ✅ **Provider/Model Whitelisting**: Security enforcement at validation layer
- ✅ **Multi-Tier Agent Routing**: Flash (<100ms) vs Pro (<1s) agents
- ✅ **Complete Audit Trail**: Immutable hash-chain logs for compliance
- ✅ **Cost Variance Tracking**: Monitor actual vs estimated costs
- ✅ **Budget Management**: Daily, monthly, per-request limits
- ✅ **Risk Assessment**: Real-time anomaly detection
- ✅ **Backend Integration**: Abstract interfaces for flexible deployment

## 🚀 Status

✅ **Partially Complete** 


**Flow**: validate → load policies → check budget → assess risk → route to agent → decide → Execute(pay)& return response.




### Brain Responsibilities

The agentic brain is the orchestrator that:
1. **Validates user** - Checks account status, verification
2. **Fetches policies** - System policies (platform rules) + User policies (preferences)
3. **Evaluates request** - Checks compliance, budget, cost estimation
4. **Assesses risk** - Detects anomalies, scores risk (1-10)
5. **Makes decision** - Approve/reject based on all checks
6. **Executes** - Calls provider APIs if approved
7. **Returns result** - Sends response + state updates to backend

All models operate in **READ-ONLY** mode - they fetch from backend, never save directly.
Backend is responsible for all state persistence.

### System Components

#### Phase 1: Core Models ✅
- **UserContext**: User validation and context
- **APIRequest**: Request structure and fetching
- **Budget**: Budget tracking models
- **Cost**: Cost calculation models
- **Decision**: Decision tracking
- **Audit**: Audit logging

#### Phase 2: Policy Engine ✅
- **PolicyManager**: Dual-layer policy enforcement
  - System policies (platform-wide, cannot override)
  - User policies (user-specific, within system bounds)
- Provider/model whitelisting
- Rate limiting enforcement
- Budget limit validation

#### Phase 3: Budget & Cost System ✅
- **BudgetTracker**: Real-time budget checking
- **SpendingMonitor**: Spending analysis and alerts
- **PricingEngine**: Cost estimation and pricing
- Cost anomaly detection
- Multi-level budget tracking (per-request, daily, monthly)
```bash
# Run comprehensive medical store chatbot demo
cd /path/to/agentic
python -m src.demo_medical_store
```

**Demo shows**:
- Simple medicine info query (Flash Agent, GPT-3.5)
- Complex medical advice (Pro Agent, GPT-4)
- Prescription image analysis (Vision model)
- Cost-optimized query (Gemini)
- Unauthorized model rejection

### 2. Basic Usage

```python
from main import AgenticBrain

# Initialize brain
brain = AgenticBrain()

# Process request
result = await brain.process_request({
    'user_id': 'user_001',
    'project_id': 'chatbot_main',
    'api_provider': 'openai',
    'model_name': 'gpt-3.5-turbo',
    'endpoint': '/chat/completions',
    'parameters': {
        'messages': [{'role': 'user', 'content': 'What is AI?'}],
        'max_tokens': 100
    },
    'estimated_tokens': 100
})

# Check result
if result['success']:
    print(f"✅ Approved - Paid ${result['payment']['actual_amount']:.4f}")
    print(f"TX: {result['payment']['payment_tx_hash']}")
else:
    print(f"❌ Rejected: {result['message']}")
```

### 3. Production Integration

See `src/example_production_backend.py` for complete integration guide.

```python
from integrations.backend_client import ProductionBackendClient, set_backend_client
from main import AgenticBrain

# Create production backend client
backend = ProductionBackendClient(
    api_base_url="https://api.yourcompany.com",
    api_key=os.environ["BACKEND_API_KEY"]
)

# Inject into brain
set_backend_client(backend)

# Use normally
brain = AgenticBrain()
result = await brain.process_request(request_data)
```

## 🧠 Decision Engine (12-Step Pipeline)

The autonomous decision engine evaluates every request through 12 steps:

1. **Validate Structure** - Check request format
2. **Load User Context** - Fetch user account info
3. **Load Policies** - Get provider/model whitelist
4. **Validate Provider/Model** - ⚠️ **CRITICAL** Enforce whitelist
5. **Estimate Cost** - Calculate expected cost
6. **Check Budget** - Verify sufficient funds
7. **Check Policy** - Verify compliance
8. **Assess Risk** - Anomaly detection
9. **Build Context** - Aggregate all data
10. **Route to Agent** - Flash (<$1, risk<5) vs Pro (≥$1 OR risk≥5)
11. **Get AI Decision** - Agent makes final decision
12. **Return Decision** - With complete audit trail

## 💰 Payment Flow

**Single blockchain transaction per request** (no refunds):

1. **Estimate Cost**: Brain calculates estimated cost
2. **Execute Payment**: Backend executes USDC TX on Arc blockchain
3. **Call Provider API**: Brain calls OpenAI/Anthropic/etc.
4. **Track Variance**: Log difference between estimated and actual cost
5. **Update Spending**: Backend updates user's budget records

**Why single TX?**
- Simpler architecture (no refund logic)
- Lower gas costs (one TX instead of multiple)
- Faster execution (no waiting for refund)
- Clear variance tracking for optimization

## 🔐 Security Features

- **Provider/Model Whitelisting**: Strict validation at Step 4
- **Budget Limits**: Daily, monthly, per-request caps
- **Risk Detection**: Real-time anomaly detection
- **Audit Trail**: Immutable hash-chain logs
- **Account Validation**: Active/suspended account checks

## 📊 Monitoring & Compliance

### Audit Trail
Every request generates complete audit trail:
- Request received
- Policy checks
- Budget checks
- Risk assessment
- Agent decision
- Payment execution
- API call results
- Errors and failures

### Compliance Reports
```python
from audit_logging.audit_logger import AuditLogger

logger = AuditLogger()
report = await logger.generate_compliance_report(
    start_time=datetime.now() - timedelta(days=30),
    end_time=datetime.now()
)

print(f"Total Requests: {report.total_requests}")
print(f"Approved: {report.approved_requests}")
print(f"Rejected: {report.rejected_requests}")
print(f"Avg Cost: ${report.average_cost:.4f}")
```



## 🎯 Key Benefits

- **80-90% Cost Savings**: Pay only for actual usage vs subscriptions
- **Complete Control**: Provider/model whitelist, budget limits
- **Full Transparency**: Every decision logged and auditable
- **Instant Flexibility**: Switch providers/models without contracts
- **Production Ready**: Complete backend integration support
- **Compliance**: Immutable audit trail for regulatory requirements

## 🔧 Configuration

Configure via environment variables or backend API:





## Request Flow

The complete system flow with automatic payment:

1. **User/Agent → Frontend**: User makes request or agent via platform link
2. **Frontend → Backend**: Submit API request (HTTP endpoint implemented by backend)
3. **Backend → Brain**: Backend calls `brain.process_request()` (direct Python function call)
4. **Brain Processing** (10 steps):
   - Create audit log
   - Validate user (account status, verification)
   - Create request object
   - Fetch policies (system + user from backend)
   - Check compliance (provider, model, rate limits)
   - Estimate cost
   - Check budget (per-request, daily, monthly)
   - Assess risk (anomaly detection, baseline comparison)
   - Make decision (approve/reject/review)
   - **If approved**: Reserve payment → Execute API → Commit payment
5. **Brain → Provider API** (if approved): Execute API call
6. **Provider API → Brain**: Return response
7. **Brain → Payment System**: Automatic payment (USDC on Arc blockchain)
8. **Brain → Backend**: Send results + payment details + state updates
9. **Backend → Database**: Update state/persistence
10. **Backend → Frontend**: Return final response with payment receipt
11. **Frontend → User**: Display result + payment confirmation

## Request Flow

The brain processes each request through 9 steps:

1. **Create Audit Log** - Initialize tracking
2. **Validate User** - Check account status, verification, active status
3. **Create Request** - Build APIRequest object
4. **Fetch Policies** - Load system policy + user policy from backend
5. **Check Compliance** - Validate against both policies (system first, then user)
6. **Estimate Cost** - Calculate expected cost based on provider/model/tokens
7. **Check Budget** - Verify sufficient budget at all levels (per-request, daily, monthly)
8. **Assess Risk** - Run anomaly detection, calculate risk score (1-10)
9. **Make Decision** - Approve/review/reject based on all checks
10. **Execute** (if approved) - Call provider API, update backend, finalize audit


