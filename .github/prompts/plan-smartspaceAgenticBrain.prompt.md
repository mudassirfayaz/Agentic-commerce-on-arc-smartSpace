# Plan: SmartSpace Agentic Brain - Complete Intelligent Governance System

**TL;DR:** Transform the agentic system from a simple payment validator into the **intelligent governance engine** powering all SmartSpace decisions. The brain must handle: (1) user context & policy enforcement with **model/provider whitelisting**, (2) budget tracking & spending limits, (3) cost estimation for **approved providers only**, (4) risk detection & anomaly prevention, (5) multi-tier autonomous decisions (Flash/Pro), (6) backend integration, and (7) comprehensive audit logging. **Agents work exclusively with user-configured providers (OpenAI, Google, Anthropic, etc.)—no arbitrary API calls allowed.** This enables true autonomous AI commerce with safety guardrails and compliance.

---

## Real-World Business Use Case: 24/7 Medical Store Chatbot

**The Scenario:**
A medical store runs a 24/7 customer chatbot that provides:
- Medicine information and recommendations
- Availability checks
- Medical guidance
- Customer support

Currently, they maintain direct integrations with OpenAI and Google Gemini, paying monthly fees regardless of usage.

**The Problem (Without SmartSpace):**
- Locked into monthly billing cycles with overlapping costs
- Cannot quickly switch to cheaper/faster/better providers
- Maintains multiple accounts and complicated reconciliation
- Cannot experiment with new models without setup friction
- Monthly bills don't match actual usage patterns

**SmartSpace Solution:**
The chatbot connects to SmartSpace instead of directly to providers.

**What happens on each customer request:**
```
1. Customer → Medical Store Chatbot → SmartSpace
2. SmartSpace validates provider/model against store's config
3. SmartSpace checks current prices and store's spending policies
4. SmartSpace reserves USDC from store's wallet
5. SmartSpace routes request to selected provider (OpenAI, Google, or another)
6. Provider returns response
7. SmartSpace logs response + actual cost + payment details
8. Store gets complete receipt with usage record
9. Response sent back to customer
```

**Business Benefits for Medical Store:**
- ✅ Pay ONLY for actual usage (per-request, not monthly)
- ✅ Switch providers instantly (no billing penalties)
- ✅ Test new models without commitment
- ✅ Centralized cost visibility and control
- ✅ No vendor lock-in or setup friction
- ✅ Complete audit trail for compliance

**Cost Comparison:**
- **Old way:** OpenAI monthly subscription ($20-100) + Gemini monthly subscription ($20-100) = $40-200/month minimum, whether they use it or not
- **SmartSpace way:** Pay per request (e.g., $0.002/request) = $2-20/month for typical 24/7 chatbot usage
- **Savings:** 80-90% reduction in AI API costs

**For Developers:**
The agentic brain handles:
1. Provider validation (only allowed providers/models)
2. Real-time pricing lookup
3. Budget enforcement
4. Spending policy enforcement
5. Automatic payment per request
6. Complete audit logging
7. Risk detection for anomalies
8. Support for instant provider switching

---

**The Golden Rule:** Agents can ONLY use providers and models that users have explicitly configured and approved. This is non-negotiable.

**How it works:**
1. When setting up a project or agent, user configures **allowed_providers** (e.g., ["openai", "anthropic", "google"])
2. For each provider, user whitelists specific **allowed_models** (e.g., openai: ["gpt-4", "gpt-3.5-turbo"])
3. When agent/user requests an API call → system validates provider + model against whitelist
4. If provider OR model is not in whitelist → **IMMEDIATE REJECTION** with clear reason
5. If both are whitelisted → proceed with cost estimation, budget checks, risk analysis, etc.

**Example scenarios:**
- ✅ User configured: openai + gpt-4 → Agent requests openai/gpt-4 → APPROVED (if other checks pass)
- ❌ User configured: openai only → Agent requests anthropic/claude → REJECTED
- ❌ User configured: openai/gpt-4 only → Agent requests openai/gpt-4-vision → REJECTED  
- ✅ User configured: openai + [gpt-4, gpt-4-vision] → Agent requests gpt-4-vision → APPROVED (if other checks pass)

**This ensures:**
- No rogue API calls to unauthorized providers
- Users maintain strict control over which AI services their agents use
- Clear audit trail of configured vs. requested providers
- Simple to extend: just add provider to whitelist to enable it

---

## Implementation Steps

### Step 1: Create Core Data Models (`src/models/`)

Define the system's common language across all components:

**Files to create:**
- `src/models/__init__.py`
- `src/models/request.py` - APIRequest, RequestStatus
- `src/models/decision.py` - ApprovalDecision, DecisionReason
- `src/models/user.py` - UserContext, UserPolicy
- `src/models/budget.py` - BudgetPolicy, BudgetStatus
- `src/models/audit.py` - AuditLog, AuditEntry
- `src/models/risk.py` - RiskAssessment, RiskScore
- `src/models/cost.py` - CostEstimate, CostComparison

**Key fields for APIRequest:**
```python
- request_id: str (unique identifier)
- user_id: str
- project_id: str
- agent_id: Optional[str]
- api_provider: str (MUST be from user's whitelist: "openai", "anthropic", "google", etc.)
- model_name: str (MUST be from user's model whitelist: "gpt-4", "claude-3-opus", etc.)
- operation_type: str (e.g., "chat", "vision", "code")
- request_params: Dict (prompt, temperature, max_tokens, etc.)
- estimated_cost: float (USDC)
- actual_cost: Optional[float]
- timestamp: datetime
- status: RequestStatus (PENDING, APPROVED, REJECTED, EXECUTED, FAILED)
- provider_whitelist_verified: bool (validated during policy check)
- model_whitelist_verified: bool (validated during policy check)
```

**Key fields for ApprovalDecision:**
```python
- decision_id: str (unique decision identifier)
- request_id: str
- status: str (APPROVE, REJECT, ESCALATE, QUARANTINE)
- reason: str (human-readable explanation)
- reasoning_details: Dict (why this decision was made)
- risk_score: float (1-10)
- agent_tier: str (FLASH or PRO)
- provider_selected: str (which provider was used, e.g., "openai")
- model_selected: str (which model was used, e.g., "gpt-4")
- estimated_cost: float (USDC, estimated before execution)
- actual_cost: Optional[float] (USDC, actual cost after execution)
- cost_variance: Optional[float] (actual - estimated, for anomaly detection)
- policies_checked: List[str] (which policies were validated)
- timestamp: datetime
- transaction_hash: Optional[str] (blockchain tx hash for USDC payment)
- receipt_id: str (link to full audit receipt)
```

---

### Step 2: Build Policy Engine (`src/policies/policy_manager.py`)

Load and enforce user-defined spending rules.

**Responsibilities:**
- Load policies from backend/database
- Validate requests against policies
- Return compliance status with violation details
- Support policy types:
  - **Allowed providers** (whitelist: e.g., "openai", "google", "anthropic")
  - **Allowed models** (whitelist specific models: e.g., "gpt-4", "claude-3-opus", "gemini-pro")
  - Per-request limits (max $X per call)
  - Forbidden providers (additional blocks on whitelisted APIs)
  - Rate limiting (X requests per minute/hour)
  - Budget caps (daily/monthly/rolling limits)
  - Spending periods (when can spending occur)
  - Recipient restrictions (allowed wallet addresses)

**Key methods:**
```python
class PolicyManager:
    async def load_policies(user_id: str, project_id: str) -> Dict[str, Policy]:
        """Load ALL policies including provider/model whitelists"""
    
    async def check_compliance(request: APIRequest, policies: Dict) -> ComplianceResult:
        """Check if request complies with ALL policies including provider/model whitelists"""
    
    async def validate_provider(provider: str, policies: Dict) -> ProviderValidation:
        """Check if provider is in user's whitelist. REJECT if not allowed."""
    
    async def validate_model(model: str, provider: str, policies: Dict) -> ModelValidation:
        """Check if model is in user's whitelist for this provider. REJECT if not allowed."""
    
    async def get_allowed_providers(user_id: str, project_id: str) -> List[str]:
        """Get list of approved providers user has configured"""
    
    async def get_allowed_models(user_id: str, project_id: str, provider: str) -> List[str]:
        """Get list of approved models for specific provider"""
    
    async def validate_per_request_limit(cost: float, policies: Dict) -> bool
    async def validate_rate_limit(user_id: str, request_count: int) -> bool
```

---

### Step 3: Implement Budget & Cost System

**File: `src/budgets/budget_tracker.py`**
- Track user/project USDC balances
- Check available budget
- Reserve budget on approval
- Update on execution
- Detect budget anomalies

**Key methods:**
```python
class BudgetTracker:
    async def get_available_balance(user_id: str, project_id: str) -> float
    async def check_sufficient_budget(user_id: str, amount: float) -> BudgetCheck
    async def get_budget_status(user_id: str, project_id: str) -> BudgetStatus
    async def get_spending_by_period(user_id: str, period: str) -> float
    async def reserve_budget(request_id: str, amount: float) -> Reservation
    async def commit_spending(request_id: str, actual_amount: float) -> Result
    async def release_reservation(request_id: str) -> Result
```

**File: `src/pricing/pricing_engine.py`**
- Query provider pricing data
- Estimate token usage
- Calculate total cost including platform fee
- Compare estimated vs. actual
- Detect cost anomalies

**Key methods:**
```python
class PricingEngine:
    async def estimate_cost(request: APIRequest) -> CostEstimate
    async def get_provider_pricing(provider: str, model: str) -> PricingData
    async def estimate_tokens(prompt: str, model: str) -> int
    async def calculate_total_cost(base_cost: float, platform_fee: float) -> float
    async def detect_cost_anomaly(actual: float, estimated: float) -> bool
    async def get_price_history(provider: str, period: str) -> List[Price]
```

---

### Step 4: Develop Risk & Anomaly Detection (`src/risk/risk_detector.py`)

Analyze requests for fraud patterns, unusual activity, suspicious behavior.

**Risk scoring system (1-10):**
- 1-2: Very low risk (routine request from known user)
- 3-4: Low risk (normal patterns)
- 5-6: Medium risk (some unusual patterns)
- 7-8: High risk (multiple red flags, escalate)
- 9-10: Critical risk (suspected fraud, block)

**Detection patterns:**
- Unusual spike in request volume
- Requests from new/unknown agents
- Cost exceeding user's typical spending
- Rate limit violations
- Repeated rejections + workarounds
- Requests to suspicious recipients
- Geographic anomalies
- Time-based anomalies

**Key methods:**
```python
class RiskDetector:
    async def analyze_request(request: APIRequest, user_context: UserContext) -> RiskAssessment
    async def calculate_risk_score(request: APIRequest, factors: List[Factor]) -> float
    async def check_fraud_indicators(request: APIRequest) -> List[Indicator]
    async def check_unusual_patterns(user_id: str, request: APIRequest) -> List[Pattern]
    async def get_user_baseline(user_id: str, period: str) -> UserBaseline
    async def compare_against_baseline(request: APIRequest, baseline: UserBaseline) -> Comparison
    async def detect_coordinated_attacks(user_id: str) -> bool
```

---

### Step 5: Enhance Gemini AI with Two-Tier System (`src/agents/`)

Redesign the agent system with two tiers of decision-making.

**Refactor `src/agents/gemini_agent.py`:**

```python
class BaseAgent:
    """Base class with common AI reasoning"""
    def __init__(self, model_name: str, system_prompt: str, temperature: float = 0.1):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
    
    async def think(self, prompt: str) -> str:
        """AI reasoning with structured output"""
        # Use Gemini's extended thinking for complex decisions
        response = await self.client.models.generate_content(...)
        return response.text

class FlashModel(BaseAgent):
    """Fast instant approval for low-risk micro-transactions (<$1.00)"""
    
    def __init__(self):
        system_prompt = """
You are the SmartSpace Flash Agent - the fast decision-maker for simple requests.
Your Goal: Process simple, low-risk API requests instantly.

RULES:
1. If cost < $1.00 AND no red flags AND within budget → APPROVE immediately
2. If cost >= $1.00 OR multiple risk flags detected → ESCALATE to Pro
3. If fraud indicators detected → REJECT
4. Be concise, efficient, no hesitation.

Always respond with JSON: {"decision": "APPROVE|REJECT|ESCALATE", "reason": "..."}
"""
        super().__init__(
            model_name="gemini-2.5-flash",
            system_prompt=system_prompt,
            temperature=0.1
        )
    
    async def decide(self, request: APIRequest, context: RequestContext) -> ApprovalDecision:
        prompt = self._build_decision_prompt(request, context)
        reasoning = await self.think(prompt)
        # Parse reasoning and build decision
        return ApprovalDecision(...)

class ProModel(BaseAgent):
    """Careful analysis for medium-value requests ($5-$100)"""
    
    def __init__(self):
        system_prompt = """
You are the SmartSpace Pro Agent - the careful analyst for medium-value requests.
Your Goal: Analyze requests thoroughly, balancing speed and caution.

ANALYSIS FRAMEWORK:
1. Validate request legitimacy
2. Verify budget and policy compliance
3. Assess risk indicators
4. Compare against historical patterns
5. Make informed decision

RULES:
- Cost $5-$100: Require thorough analysis
- Multiple violations: REJECT
- Fraud indicators: REJECT immediately
- Unknown/new agent: ESCALATE if cost >$50

Response JSON: {"decision": "APPROVE|REJECT|ESCALATE", "reasoning": {...}, "conditions": [...]}
"""
        super().__init__(
            model_name="gemini-2.5-flash",  # Upgrade to pro later
            system_prompt=system_prompt,
            temperature=0.2
        )
    
    async def decide(self, request: APIRequest, context: RequestContext) -> ApprovalDecision:
        # Multi-step reasoning
        analysis = await self._analyze_legitimacy(request, context)
        risk_check = await self._check_risks(request, context)
        policy_check = await self._check_policies(request, context)
        decision = await self._synthesize_decision(analysis, risk_check, policy_check)
        return decision

```

---

### Step 6: Build Clean Backend Interface (`src/backend_interface/`)

Abstract payment execution and external integrations.

**File: `src/backend_interface/backend_client.py`**
```python
class BackendClient:
    """Interface to SmartSpace backend for all external operations"""
    
    async def get_user_context(user_id: str) -> UserContext:
        """Load user/project/agent config from backend"""
        
    async def query_cost(provider: str, model: str, params: Dict) -> float:
        """Query actual cost from provider"""
        
    async def execute_payment(decision: ApprovalDecision) -> PaymentResult:
        """Execute USDC payment (pending Arc/Circle integration)"""
        
    async def log_audit_entry(entry: AuditEntry) -> Result:
        """Store audit log in database"""
        
    async def update_user_budget(user_id: str, amount: float) -> Result:
        """Update user's remaining budget"""
        
    async def call_external_api(request: APIRequest) -> APIResult:
        """Call the actual external API via SmartSpace gateway"""
```

**File: `src/backend_interface/payment_executor.py`**
```python
class PaymentExecutor:
    """Executes approved payments via Arc/Circle (pending integration)"""
    
    async def approve_payment(
        user_id: str,
        amount: float,
        recipient: str,
        request_id: str,
        reason: str
    ) -> PaymentResult:
        """
        Execute USDC payment on Arc blockchain
        
        Returns: {
            "status": "success" | "pending" | "failed",
            "transaction_hash": str,
            "amount": float,
            "timestamp": datetime
        }
        """
        
    async def get_payment_status(tx_hash: str) -> PaymentStatus:
        """Check blockchain confirmation status"""
        
    async def handle_payment_failure(tx_hash: str, error: str) -> Result:
        """Handle failed payments, implement retries"""
```

---

### Step 7: Create Comprehensive Audit System (`src/logging/audit_logger.py`)

Log every decision with full context for compliance.

**Key requirements:**
- Immutable logs (append-only)
- Full timestamp precision
- Complete context (user, agent, policies, reasoning)
- Support compliance reports
- Data retention policies
- Query capabilities

```python
class AuditLogger:
    """Comprehensive audit logging for compliance and debugging"""
    
    async def log_request_received(request: APIRequest) -> None:
        """Log incoming request"""
        
    async def log_policy_check(request_id: str, policies: List[str], results: Dict) -> None:
        """Log policy validation results"""
        
    async def log_risk_assessment(request_id: str, assessment: RiskAssessment) -> None:
        """Log risk analysis details"""
        
    async def log_agent_decision(
        request_id: str,
        agent_tier: str,
        decision: ApprovalDecision,
        reasoning: str
    ) -> None:
        """Log agent's reasoning and decision"""
        
    async def log_payment_execution(
        request_id: str,
        amount: float,
        tx_hash: str,
        status: str
    ) -> None:
        """Log payment execution"""
        
    async def log_api_execution(
        request_id: str,
        result: APIResult,
        actual_cost: float
    ) -> None:
        """Log external API call result"""
        
    async def get_request_audit_trail(request_id: str) -> AuditTrail:
        """Retrieve full audit trail for a request"""
        
    async def generate_compliance_report(
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> ComplianceReport:
        """Generate compliance-ready report"""
```

**Audit log entry structure:**
```python
{
    "log_id": "uuid",
    "timestamp": "2026-01-11T10:30:45.123Z",
    "request_id": "req_123",
    "user_id": "user_456",
    "project_id": "proj_789",
    "agent_id": "agent_101",
    "event_type": "policy_check|risk_assessment|agent_decision|payment_execution",
    "event_details": {...},
    "context_snapshot": {...},
    "result": "success|failure",
    "error": null,
    "hash": "sha256(previous_hash + this_entry)"  // For immutability
}
```

---

### Step 8: Implement Decision Engine (`src/decision_engine/payment_decision_engine.py`)

Orchestrate the complete autonomous payment decision flow.

```python
class AutonomousPaymentDecisionEngine:
    """
    The core decision engine coordinating all components.
    Ensures deterministic, auditable, policy-compliant decisions.
    """
    
    def __init__(self):
        self.policy_manager = PolicyManager()
        self.budget_tracker = BudgetTracker()
        self.pricing_engine = PricingEngine()
        self.risk_detector = RiskDetector()
        self.backend_client = BackendClient()
        self.audit_logger = AuditLogger()
        
        self.flash_agent = FlashModel()
        self.pro_agent = ProModel()
        self.provider_validator = ProviderValidator()
    
    async def process_request(self, request: APIRequest) -> ApprovalDecision:
        """
        Main decision pipeline - orchestrates all checks and AI reasoning.
        
        Flow:
        1. Validate request structure
        2. Load user context & policies
        3. Estimate cost
        4. Check budget availability
        5. Validate against policies
        6. Assess risk
        7. Route to appropriate agent tier
        8. Get AI decision
        9. Log everything
        10. Execute payment if approved
        11. Return decision with receipt
        """
        
        # Step 1: Validate request
        validation = await self._validate_request_structure(request)
        if not validation.valid:
            await self.audit_logger.log_validation_failure(request, validation.error)
            return ApprovalDecision(
                status="REJECT",
                reason=f"Invalid request: {validation.error}"
            )
        
        # Step 2: Load user context
        user_context = await self.backend_client.get_user_context(request.user_id)
        policies = await self.policy_manager.load_policies(
            request.user_id,
            request.project_id
        )
        
        # Step 2.5: CRITICAL - Validate provider/model are in user's whitelist
        provider_model_check = await self.provider_validator.validate_request_provider_model(
            request,
            policies
        )
        if not provider_model_check.valid:
            await self.audit_logger.log_provider_model_rejection(request, provider_model_check.reason)
            return ApprovalDecision(
                status="REJECT",
                reason=provider_model_check.reason,
                rejection_type="UNAUTHORIZED_PROVIDER_OR_MODEL"
            )
        
        # Step 3: Estimate cost
        cost_estimate = await self.pricing_engine.estimate_cost(request)
        request.estimated_cost = cost_estimate.total
        
        # Step 4: Check budget
        budget_check = await self.budget_tracker.check_sufficient_budget(
            request.user_id,
            cost_estimate.total
        )
        if not budget_check.sufficient:
            await self.audit_logger.log_budget_check(request, budget_check)
            return ApprovalDecision(
                status="REJECT",
                reason=f"Insufficient budget. Available: ${budget_check.available}, Required: ${cost_estimate.total}"
            )
        
        # Step 5: Check policies
        policy_check = await self.policy_manager.check_compliance(request, policies)
        if not policy_check.compliant:
            await self.audit_logger.log_policy_check(request, policy_check)
            return ApprovalDecision(
                status="REJECT",
                reason=f"Policy violation: {policy_check.violations[0]}"
            )
        
        # Step 6: Assess risk
        risk_assessment = await self.risk_detector.analyze_request(request, user_context)
        risk_score = risk_assessment.score
        
        # Step 7: Route to agent tier
        request_context = RequestContext(
            user_context=user_context,
            policies=policies,
            cost_estimate=cost_estimate,
            budget_check=budget_check,
            policy_check=policy_check,
            risk_assessment=risk_assessment
        )
        
        # Route based on cost and risk
        if cost_estimate.total < 1.00 and risk_score < 5:
            agent_tier = "FLASH"
            agent = self.flash_agent
        else:
            # All higher costs or higher risk go to Pro
            agent_tier = "PRO"
            agent = self.pro_agent
        
        # Step 8: Get AI decision
        decision = await agent.decide(request, request_context)
        decision.agent_tier = agent_tier
        decision.risk_score = risk_score
        
        # Step 9: Log decision
        await self.audit_logger.log_agent_decision(
            request.request_id,
            agent_tier,
            decision,
            decision.reasoning_details
        )
        
        # Step 10: Execute payment if approved
        if decision.status == "APPROVE":
            payment_result = await self.backend_client.execute_payment(decision)
            decision.transaction_hash = payment_result.tx_hash
            await self.audit_logger.log_payment_execution(request, payment_result)
        
        # Step 11: Return decision with receipt
        receipt = await self._generate_receipt(request, decision)
        decision.receipt = receipt
        
        return decision
    
    async def _validate_request_structure(self, request: APIRequest) -> ValidationResult:
        """Validate request has all required fields"""
        
    async def _generate_receipt(self, request: APIRequest, decision: ApprovalDecision) -> Receipt:
        """Generate receipt with all details for user"""
```

---

### Step 9: Add Provider & Model Validation Logic (`src/providers/provider_validator.py`)

Enforce strict whitelist control over which providers/models agents can access.

```python
class ProviderValidator:
    """
    CRITICAL: Ensure agents ONLY work with user-approved providers and models.
    All API requests must match user's configured whitelist.
    """
    
    async def validate_request_provider_model(
        request: APIRequest,
        policies: Dict
    ) -> ValidationResult:
        """
        MANDATORY CHECK: Verify provider and model are in user's whitelist.
        
        Rejects if:
        - Provider not in allowed_providers list
        - Model not in allowed_models list for that provider
        - User is trying to use arbitrary/unauthorized API
        
        Returns: {"valid": bool, "reason": str if invalid}
        """
    
    async def get_allowed_providers_for_user(
        user_id: str,
        project_id: str
    ) -> List[ProviderConfig]:
        """Get all providers user has configured and approved"""
        
    async def get_allowed_models_for_provider(
        user_id: str,
        project_id: str,
        provider: str
    ) -> List[str]:
        """Get all models approved for specific provider"""
    
    async def check_provider_health(provider: str) -> HealthStatus:
        """Check if approved provider API is available"""
    
    async def get_fallback_provider(
        user_id: str,
        project_id: str,
        original_provider: str,
        reason: str
    ) -> Optional[str]:
        """Get fallback provider from user's whitelist if primary fails"""
    
    async def reject_unauthorized_provider(
        request: APIRequest,
        reason: str
    ) -> RejectionReason:
        """Return clear reason for rejecting unauthorized provider/model combo"""
```

**Decision Flow for Provider/Model Whitelist:**
```
Agent receives request → api_provider="openai", model_name="gpt-4"
        ↓
Load user's allowed_providers policy for this project
        ↓
Is "openai" in allowed_providers?
    ├─ NO → REJECT: "OpenAI not configured for this project"
    └─ YES → Continue
        ↓
Load user's allowed_models["openai"] list from policy
        ↓
Is "gpt-4" in allowed_models["openai"]?
    ├─ NO → REJECT: "GPT-4 not approved. Available: gpt-3.5-turbo, gpt-4-vision"
    └─ YES → APPROVE provider/model combo, proceed with cost estimation
        ↓
All subsequent checks (budget, risk, compliance) can proceed
```

**Example Policy Configuration:**
```json
{
  "allowed_providers": ["openai", "anthropic", "google"],
  "allowed_models": {
    "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-vision"],
    "anthropic": ["claude-3-opus", "claude-3-sonnet"],
    "google": ["gemini-pro", "gemini-pro-vision"]
  },
  "forbidden_operations": ["openai.gpt-4.batch-processing"],
  "per_request_limit": 10.00,
  "daily_budget": 100.00,
  "rate_limit_per_minute": 10
}
```

---

### Step 10: Refactor Main Orchestrator (`main.py` + `src/tasks/processor.py`)

Simplify to call the decision engine.

**Refactored `main.py`:**
```python
"""
SmartSpace Agentic System - Main Entry Point
Real-world example: 24/7 Medical Store Chatbot

A pharmacy uses SmartSpace to power their customer chatbot.
They've configured:
- Allowed providers: OpenAI, Google Gemini
- OpenAI models: gpt-4, gpt-3.5-turbo
- Google models: gemini-pro
- Daily budget: $50 USDC
- Per-request limit: $1 USDC
"""

from src.decision_engine.payment_decision_engine import AutonomousPaymentDecisionEngine
from src.models.request import APIRequest

async def main():
    """
    Demonstrates the agentic brain processing medical store chatbot requests
    """
    
    engine = AutonomousPaymentDecisionEngine()
    
    # Medical store project configuration
    medical_store_user_id = "medical_store_001"
    medical_store_project_id = "chatbot_24_7"
    
    # Test scenarios representing real chatbot conversations
    scenarios = [
        {
            "name": "Customer asks medicine info - Quick response",
            "description": "Customer: 'What's the side effect of Ibuprofen?'",
            "request": APIRequest(
                user_id=medical_store_user_id,
                project_id=medical_store_project_id,
                api_provider="openai",
                model_name="gpt-3.5-turbo",
                operation_type="chat",
                request_params={"prompt": "What are side effects of Ibuprofen? Be concise.", "max_tokens": 150},
                estimated_cost=0.002
            )
        },
        {
            "name": "Customer asks detailed advice - Use better model",
            "description": "Customer: 'Which medicine should I take for fever with headache?'",
            "request": APIRequest(
                user_id=medical_store_user_id,
                project_id=medical_store_project_id,
                api_provider="openai",
                model_name="gpt-4",
                operation_type="chat",
                request_params={"prompt": "Patient has fever + headache. Recommend appropriate OTC medicines.", "max_tokens": 300},
                estimated_cost=0.08
            )
        },
        {
            "name": "Customer shares prescription image - Vision analysis",
            "description": "Customer uploads prescription image for verification",
            "request": APIRequest(
                user_id=medical_store_user_id,
                project_id=medical_store_project_id,
                api_provider="openai",
                model_name="gpt-4-vision",
                operation_type="vision",
                request_params={"image_url": "prescription_image.jpg", "prompt": "Extract medicine names and dosages from this prescription"},
                estimated_cost=0.15
            )
        },
        {
            "name": "Provider switching - Use Google Gemini for cost optimization",
            "description": "Fallback to Google Gemini for better pricing",
            "request": APIRequest(
                user_id=medical_store_user_id,
                project_id=medical_store_project_id,
                api_provider="google",
                model_name="gemini-pro",
                operation_type="chat",
                request_params={"prompt": "Is Aspirin suitable for children? Provide safety guidelines.", "max_tokens": 200},
                estimated_cost=0.001
            )
        },
        {
            "name": "Unauthorized provider - Rejection",
            "description": "Chatbot tries to use Anthropic (not in store's whitelist)",
            "request": APIRequest(
                user_id=medical_store_user_id,
                project_id=medical_store_project_id,
                api_provider="anthropic",
                model_name="claude-3-opus",
                operation_type="chat",
                request_params={"prompt": "..."},
                estimated_cost=0.20
            )
        },
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"📋 Scenario: {scenario['name']}")
        print(f"{'='*60}")
        
        decision = await engine.process_request(scenario["request"])
        
        print(f"Status: {decision.status}")
        print(f"Reason: {decision.reason}")
        print(f"Risk Score: {decision.risk_score}/10")
        print(f"Agent Tier: {decision.agent_tier}")
        print(f"Cost Approved: ${decision.cost_approved}")
        print(f"Audit ID: {decision.receipt.audit_trail_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## Further Considerations

### 1. Determinism & Reproducibility

**Requirement:** Same input + same policies + same system state = same decision every time

**Implementation:**
- Create request fingerprint: `hash(request + user_policies + cost_snapshot + risk_baseline)`
- Store fingerprint in audit log
- Enable decision replay/verification
- Document all sources of non-determinism (e.g., time-based windows)

**Questions:**
- Should we cache decisions for identical requests? (Pro: speed, Con: stale context)
- How often should we update baselines for risk detection?
- What's acceptable variance in cost estimates across runs?

---

**Two-Tier Agent Strategy**

**Current Design:**
- **FlashModel:** <$1.00, no risk flags → instant approval
- **ProModel:** >=$1.00 or risk flags detected → careful analysis

**Escalation Triggers to Humans (from ProModel):**
- Risk score > 7
- Policy violations detected
- Fraud indicators present
- System uncertainty/edge cases
- Enterprise override requests
- High-value requests (>$100)

**Questions:**
- When should ProModel escalate to human vs. auto-reject?
- Should we implement multiple ProModel calls for very high values (consensus)?
- What's acceptable latency? (Flash: <100ms, Pro: <1s)
- Should Flash model cache decisions for identical requests?

---

### 3. Backend Integration Sequencing

**Phase 1 (Now):** Mock implementations with clear interfaces
- Mock `BackendClient.get_user_context()` 
- Mock `BackendClient.query_cost()`
- Mock `PaymentExecutor.approve_payment()`

**Phase 2 (Backend Ready):** Swap in real implementations
- Integrate with SmartSpace backend API
- Query real cost from providers
- Real USDC balance checks

**Phase 3 (Arc/Circle Ready):** Web3 payment execution
- Real blockchain transactions
- Handle confirmation delays
- Manage nonce/replay protection

**Key Decisions:**
- Sync or async payment execution? (Async recommended for blockchain)
- How long to wait for payment confirmation? (Use timeout + polling)
- What if payment fails after AI approval? (Retry logic, user notification)

---

### 4. Safety Guardrails

**Hard Limits (System-wide):**
- Max single request: $1000 (cannot override)
- Max daily spend per user: $10,000 (cannot override)
- Max agents per project: 100 (system limit)

**Soft Limits (User-configurable):**
- Warnings at 80% of budget
- Policy violation alerts
- Anomaly detection triggers

**Kill Switch:**
- User can revoke agent permissions immediately
- Admin can freeze account for investigation
- Automatic freeze on repeated rejections (signs of abuse)

---

### 5. Audit & Compliance

**Requirements:**
- Immutable append-only logs
- Full context for every decision
- Data retention per legal requirements
- GDPR right-to-be-forgotten support
- SOC 2 Type II compliance
- PCI-DSS for payment data (if applicable)

**Log Retention:**
- Active requests: 7 days
- Completed transactions: 7 years
- Audit entries: 2 years minimum
- Support for legal holds

**Compliance Reports:**
- Daily activity summaries
- Policy violation reports
- Anomaly investigation reports
- Regulatory audit trails

---

## Architecture Diagram

```
User Request
    ↓
┌─────────────────────────────────┐
│ Request Validation & Structure  │
└─────────────────┬───────────────┘
                  ↓
┌─────────────────────────────────┐
│ Load User Context & Policies    │
└─────────────────┬───────────────┘
                  ↓
┌─────────────────────────────────┐
│ Cost Estimation                 │
└─────────────────┬───────────────┘
                  ↓
┌─────────────────────────────────┐
│ Budget Availability Check       │
└─────────────────┬───────────────┘
                  ↓
┌─────────────────────────────────┐
│ Policy Compliance Check         │
└─────────────────┬───────────────┘
                  ↓
┌─────────────────────────────────┐
│ Risk & Anomaly Detection        │
└─────────────────┬───────────────┘
                  ↓
     ┌────────────┴────────────┐
     ↓                         ↓
 Risk < 3              Risk 3-7              Risk > 7
     ↓                         ↓                 ↓
┌─────────┐           ┌──────────┐         ┌──────────┐
│ FLASH   │           │   PRO    │         │ AUDITOR  │
│ Model   │           │  Model   │         │  Model   │
└────┬────┘           └────┬─────┘         └────┬─────┘
     ↓                     ↓                     ↓
  Decision             Decision               Decision
     │                     │                     │
     └─────────────────────┴─────────────────────┘
                           ↓
                    ┌──────────────┐
                    │ Log Decision │
                    │ (Audit Trail)│
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Execute      │
                    │ Payment      │
                    │ (if APPROVE) │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Generate     │
                    │ Receipt      │
                    └──────┬───────┘
                           ↓
                    Approval Decision
                    + Receipt + Audit Trail
```

---

## Success Criteria

When complete, the agentic system should:

1. ✅ **Handle all SmartSpace decisions** - Not just payments, but policies, budgets, risk
2. ✅ **Enforce safety guardrails** - Hard limits, policy compliance, fraud prevention
3. ✅ **Provide full audit trails** - Immutable logs of every decision for compliance
4. ✅ **Support autonomous agents** - Agents can make decisions without human intervention
5. ✅ **Integrate cleanly with backend** - Clear interfaces for future Arc/Circle integration
6. ✅ **Use robust AI reasoning** - Two-tier Gemini agents (Flash/Pro) with safety guardrails
7. ✅ **Return clear receipts** - Structured receipts with all details for users
8. ✅ **Ensure determinism** - Same input always produces same decision
9. ✅ **Scale to production** - Handle high throughput, support monitoring/alerting
10. ✅ **Support compliance** - GDPR, SOC 2, audit-ready, full traceability

---

## End-to-End Flow: Medical Store Chatbot Example

To illustrate how all components work together, let's trace the medical store chatbot through each scenario:

### Scenario 1: Simple Medicine Information Query
```
User: "What are the side effects of Ibuprofen?"

┌─ STEP 1: Request Received ─────────────────────┐
│ Provider: "openai"                             │
│ Model: "gpt-3.5-turbo"                         │
│ Cost Estimate: $0.002                          │
│ Risk Profile: routine query from known app     │
└────────────────────────────────────────────────┘
                     ↓
┌─ STEP 2.5: Provider/Model Validation ────────┐
│ Check: openai in allowed_providers? ✅        │
│ Check: gpt-3.5-turbo in allowed_models? ✅   │
│ Whitelist: PASSED                              │
└────────────────────────────────────────────────┘
                     ↓
┌─ STEP 3: Budget Check ──────────────────────┐
│ User Budget: $50/day                          │
│ Today's Spending: $1.24                       │
│ Available: $48.76                             │
│ Request Cost: $0.002                          │
│ Result: ✅ APPROVED                           │
└────────────────────────────────────────────────┘
                     ↓
┌─ STEP 4: Policy Compliance ────────────────┐
│ Rate Limit: 10 req/min → Current: 3 ✅     │
│ Per-Request Max: $1.00 → Request: $0.002 ✅│
│ Daily Cap: $50 → On track ✅                │
│ All Policies: PASSED                        │
└────────────────────────────────────────────────┘
                     ↓
┌─ STEP 5: Risk Assessment ─────────────────┐
│ Request volume: normal                      │
│ Cost: within usual range                    │
│ Provider: trusted (OpenAI)                  │
│ User pattern: routine                       │
│ Risk Score: 2/10 (very low)                │
└────────────────────────────────────────────────┘
                     ↓
┌─ STEP 6: Agent Routing ───────────────────┐
│ Cost: $0.002 < $1.00? YES                  │
│ Risk: 2 < 5? YES                           │
│ Route to: FLASH Agent (instant approval)   │
└────────────────────────────────────────────┘
                     ↓
┌─ STEP 7: Flash Agent Decision ────────────┐
│ Analysis: Simple factual query              │
│ Compliance: All checks passed               │
│ Confidence: 99%                             │
│ Decision: ✅ APPROVE                       │
│ Time: 45ms                                  │
└────────────────────────────────────────────┘
                     ↓
┌─ STEP 8: Payment Execution ───────────────┐
│ Approve USDC payment: $0.002                │
│ Blockchain: Arc Network                     │
│ Transaction Hash: 0x3f8d2e...              │
│ Status: Confirmed                           │
│ Receipt ID: rcpt_20260111_001               │
└────────────────────────────────────────────┘
                     ↓
┌─ STEP 9: API Execution ───────────────────┐
│ Call: openai.gpt-3.5-turbo                 │
│ Prompt: "Side effects of Ibuprofen..."     │
│ Response: "Ibuprofen may cause..."         │
│ Actual Cost: $0.0018 (tracked)             │
│ Status: ✅ Success                         │
└────────────────────────────────────────────┘
                     ↓
┌─ STEP 10: Audit Logging ──────────────────┐
│ Log Entry: {                                │
│   request_id: "req_20260111_001",          │
│   decision: "APPROVE",                      │
│   agent_tier: "FLASH",                      │
│   provider: "openai",                       │
│   model: "gpt-3.5-turbo",                  │
│   estimated_cost: 0.002,                    │
│   actual_cost: 0.0018,                      │
│   risk_score: 2,                            │
│   tx_hash: "0x3f8d2e...",                  │
│   timestamp: "2026-01-11T10:30:45Z"        │
│ }                                           │
└────────────────────────────────────────────┘
                     ↓
            ✅ SUCCESS - Response sent to chatbot
            User receives answer in <100ms
```

### Scenario 2: Complex Medical Advice Request
```
User: "I have fever and headache. What medicine should I take?"

┌─ STEP 1-5: Same as above ─────────────────────┐
│ But: Cost Estimate: $0.08 (gpt-4, more capable)
│ Risk Score: 3/10 (slightly higher, more important)
└────────────────────────────────────────────────┘
                     ↓
┌─ STEP 6: Agent Routing ───────────────────┐
│ Cost: $0.08 < $1.00? YES                   │
│ Risk: 3 < 5? YES                           │
│ Route to: FLASH Agent                      │
│ BUT: Cost is 40x more than usual...        │
└────────────────────────────────────────────┘
                     ↓
┌─ STEP 7: Flash Agent Decision ────────────┐
│ Analysis: Moderate medical advice           │
│ Complexity: Requires multi-factor reasoning │
│ Decision: ESCALATE to Pro Agent            │
│ Reason: "Higher cost + medical domain"     │
│ Time: 60ms                                 │
└────────────────────────────────────────────┘
                     ↓
┌─ STEP 7b: Pro Agent Decision ─────────────┐
│ Analysis:                                   │
│  - Fever + Headache is common condition     │
│  - OTC advice is safe (acetaminophen,      │
│    ibuprofen, or both)                     │
│  - No red flags (not seeking diagnosis)    │
│ Confidence: 95%                            │
│ Decision: ✅ APPROVE                       │
│ Time: 200ms                                │
└────────────────────────────────────────────┘
                     ↓
      [Payment → Execution → Audit Logging]
                     ↓
            ✅ SUCCESS - Response sent to chatbot
            User receives comprehensive advice
```

### Scenario 3: Prescription Image Analysis (Vision)
```
User: [Uploads prescription image]

┌─ REQUEST DETAILS ─────────────────────────────┐
│ Provider: "openai"                            │
│ Model: "gpt-4-vision"                        │
│ Cost Estimate: $0.15                          │
│ Type: Image processing (higher cost)          │
│ Risk: 5/10 (medium - image data + analysis)  │
└───────────────────────────────────────────────┘
                     ↓
┌─ STEP 2.5: Provider/Model Validation ────────┐
│ Check: openai in allowed_providers? ✅       │
│ Check: gpt-4-vision in allowed_models? ✅   │
│ Whitelist: PASSED                            │
└───────────────────────────────────────────────┘
                     ↓
┌─ STEP 6: Agent Routing ───────────────────┐
│ Cost: $0.15 > $1.00? NO (but close)        │
│ Risk: 5 >= 5? YES                          │
│ Route to: PRO Agent (because risk = 5)     │
└───────────────────────────────────────────┘
                     ↓
┌─ PRO AGENT ANALYSIS ──────────────────────┐
│ Consider:                                  │
│ - Image contains medication info           │
│ - User wants to verify prescription        │
│ - Legitimate medical use case              │
│ - No suspicious patterns                   │
│ Confidence: 98%                            │
│ Decision: ✅ APPROVE                       │
│ Time: 250ms                                │
└───────────────────────────────────────────┘
                     ↓
      [Payment → Vision API Call → Audit]
                     ↓
  System extracts medicine names and dosages
  Returns structured data to pharmacy staff
```

### Scenario 4: Automatic Provider Switching
```
Situation: OpenAI hitting rate limits, need to switch to Gemini

┌─ ORIGINAL REQUEST ────────────────────────────┐
│ Provider: "openai"                            │
│ Model: "gpt-4"                               │
│ Cost: $0.08                                  │
│ But: OpenAI returning 429 (rate limited)     │
└───────────────────────────────────────────────┘
                     ↓
┌─ PROVIDER HEALTH CHECK ───────────────────┐
│ Check openai availability: TIMEOUT         │
│ Check: Has user configured fallback? YES   │
│ Allowed providers: openai, google          │
│ Allowed models: gpt-4, gemini-pro         │
└───────────────────────────────────────────┘
                     ↓
┌─ FALLBACK SELECTION ──────────────────────┐
│ Try: google/gemini-pro                    │
│ Cost: $0.001 (10x cheaper!)              │
│ Status: Available ✅                      │
│ Compatibility: Comparable (both LLMs)     │
│ Auto-switch: APPROVED                     │
└───────────────────────────────────────────┘
                     ↓
┌─ UPDATED REQUEST ─────────────────────────┐
│ Original: openai/gpt-4 ($0.08)            │
│ Switched: google/gemini-pro ($0.001)      │
│ Savings: $0.079                           │
│ Audit Log: "Auto-switched due to timeout" │
└───────────────────────────────────────────┘
                     ↓
      [All checks pass with new provider]
                     ↓
    ✅ SUCCESS - Request processed via Gemini
    Medical store saves 90% on this request
```

### Scenario 5: Unauthorized Provider Rejection
```
Scenario: Chatbot tries to use Anthropic (not configured)

┌─ SUSPICIOUS REQUEST ──────────────────────────┐
│ Provider: "anthropic"                         │
│ Model: "claude-3-opus"                       │
│ Cost: $0.20                                  │
│ Red Flag: Provider not in configured list    │
└───────────────────────────────────────────────┘
                     ↓
┌─ STEP 2.5: Provider/Model Validation ────────┐
│ Check: anthropic in allowed_providers? ❌   │
│ Allowed: ["openai", "google"]               │
│ Requested: "anthropic"                       │
│ Result: IMMEDIATE REJECTION                  │
└───────────────────────────────────────────────┘
                     ↓
┌─ REJECTION DETAILS ───────────────────────┐
│ Status: REJECT                             │
│ Reason: "Unauthorized provider"            │
│ Message: "Anthropic not configured. Enable │
│  it in project settings if you want to use │
│  Claude models."                           │
│ Allowed Providers: openai, google          │
└───────────────────────────────────────────┘
                     ↓
┌─ AUDIT LOGGING ───────────────────────────┐
│ Event: "Unauthorized provider attempt"    │
│ Request ID: req_20260111_005               │
│ Requested: anthropic/claude-3-opus        │
│ Status: BLOCKED                            │
│ Risk Score: 6/10 (indicates misconfiguration or abuse)
│ Action: Alert admin + log + reject         │
└───────────────────────────────────────────┘
                     ↓
        ❌ REJECTED - No cost incurred
        ❌ No USDC charged to user
        ✅ Integrity maintained - only configured providers allowed
```

---

## Real-World Impact: Medical Store Economics

**Before SmartSpace:**
- OpenAI subscription: $20/month minimum
- Google Gemini subscription: $20/month minimum
- Anthropic Claude subscription: $20/month minimum
- Daily usage: Low utilization (unused capacity)
- **Total monthly cost: $60-100 minimum**
- Per-request actual cost: ~$0.01-0.20
- Ratio: 60-100x markup

**With SmartSpace:**
- Setup: 5 minutes (configure providers, set budget)
- Daily usage: ~2,000 requests
- Average per-request cost: $0.003
- Daily spend: $6/day
- **Total monthly cost: ~$180 (pay-per-use)**
- Per-request actual cost: Same ~$0.003
- **Savings: 67-80% reduction in costs**

**Plus Benefits:**
- ✅ Instant provider switching (if one goes down)
- ✅ Automatic cost optimization (use cheapest provider that meets needs)
- ✅ Complete audit trail (who used what, when, why)
- ✅ Spending controls (daily budgets, rate limits)
- ✅ No lock-in (can change providers anytime)
- ✅ Transparent costs (know exact price per request)

---

## Next Steps

1. **Create data models** - Define all core types
2. **Build policy engine** - Load and validate policies
3. **Implement budget tracker** - Track spending and limits
4. **Develop risk detector** - Analyze requests for anomalies
5. **Refactor agents** - Add multi-tier reasoning
6. **Create audit logger** - Log every decision
7. **Build decision engine** - Orchestrate the flow
8. **Add provider selection** - Support multiple APIs
9. **Integrate backend** - Connect to external systems
10. **Test end-to-end** - Validate with real scenarios
