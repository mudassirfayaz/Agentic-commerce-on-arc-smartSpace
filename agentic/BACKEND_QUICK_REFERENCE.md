# Backend Integration Quick Reference

**For Backend Developers** - Quick guide to integrate the SmartSpace Agentic Brain

---

## 🎯 What You Need to Do

Implement the `BackendClient` interface to connect the brain to your services.

---

## 📋 Required Backend APIs

### 1. User Service

**Endpoint**: `GET /api/v1/users/{user_id}`

**Response**:
```json
{
  "user_id": "user_001",
  "account_status": "active",
  "tier": "pro",
  "total_spending": 1250.50,
  "available_balance": 874.50,
  "total_requests": 15432,
  "created_at": "2024-01-15T10:30:00Z",
  "last_request_at": "2024-12-20T14:22:10Z"
}
```

### 2. Budget Service

**Endpoint**: `GET /api/v1/users/{user_id}/projects/{project_id}/budget`

**Response**:
```json
{
  "daily_limit": 100.00,
  "monthly_limit": 1000.00,
  "per_request_limit": 10.00,
  "current_daily_spending": 45.23,
  "current_monthly_spending": 623.45,
  "period_start": "2024-12-01T00:00:00Z",
  "period_end": "2024-12-31T23:59:59Z"
}
```

### 3. Policy Service

**Endpoint**: `GET /api/v1/users/{user_id}/projects/{project_id}/policies`

**Response**:
```json
{
  "allowed_providers": ["openai", "anthropic", "google"],
  "allowed_models": {
    "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-vision"],
    "anthropic": ["claude-3-sonnet", "claude-3-haiku"],
    "google": ["gemini-pro", "gemini-pro-vision"]
  },
  "rate_limits": {
    "requests_per_minute": 60,
    "tokens_per_hour": 1000000
  },
  "forbidden_operations": ["delete", "modify_user"],
  "require_approval_above": 5.00
}
```

### 4. Pricing Service

**Endpoint**: `GET /api/v1/providers/{provider}/models/{model}/cost`

**Response**:
```json
{
  "provider": "openai",
  "model": "gpt-4",
  "input_cost_per_1k": 0.03,
  "output_cost_per_1k": 0.06,
  "updated_at": "2024-12-20T14:00:00Z"
}
```

### 5. Payment Service

**Endpoint**: `POST /api/v1/payments/execute`

**Request**:
```json
{
  "user_id": "user_001",
  "amount": 0.0234,
  "currency": "USDC",
  "network": "arc",
  "metadata": {
    "request_id": "req_abc123",
    "provider": "openai",
    "model": "gpt-4"
  }
}
```

**Response**:
```json
{
  "success": true,
  "tx_hash": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb4",
  "block_number": 18234567,
  "amount_paid": 0.0234,
  "gas_used": 21000,
  "timestamp": "2024-12-20T14:22:10Z"
}
```

**Endpoint**: `GET /api/v1/payments/{tx_hash}/status`

**Response**:
```json
{
  "tx_hash": "0x742d35Cc...",
  "status": "confirmed",
  "confirmations": 12,
  "block_number": 18234567,
  "timestamp": "2024-12-20T14:22:10Z"
}
```

### 6. Spending Service

**Endpoint**: `POST /api/v1/users/{user_id}/projects/{project_id}/spending`

**Request**:
```json
{
  "amount": 0.0234,
  "request_id": "req_abc123",
  "timestamp": "2024-12-20T14:22:15Z"
}
```

**Response**:
```json
{
  "success": true
}
```

### 7. Audit Service

**Endpoint**: `POST /api/v1/audit/logs`

**Request**:
```json
{
  "request_id": "req_abc123",
  "audit_data": {
    "events": [...],
    "trail": {...}
  },
  "timestamp": "2024-12-20T14:22:20Z"
}
```

**Response**:
```json
{
  "success": true
}
```

### 8. Provider Gateway

**Endpoint**: `POST /api/v1/providers/{provider}/call`

**Request**:
```json
{
  "endpoint": "/chat/completions",
  "payload": {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "id": "chatcmpl-...",
    "choices": [...],
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 25,
      "total_tokens": 35
    }
  },
  "cost": {
    "input_cost": 0.0003,
    "output_cost": 0.0015,
    "total_cost": 0.0018
  }
}
```

---

## 💻 Implementation Template

```python
import httpx
from integrations.backend_client import (
    BackendClient,
    BackendUserContext,
    BackendBudgetInfo,
    BackendPolicyConfig,
    BackendPaymentResult,
    BackendProviderCost
)

class ProductionBackendClient(BackendClient):
    def __init__(self, api_base_url: str, api_key: str):
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.client = httpx.AsyncClient()
    
    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}
    
    async def get_user_context(self, user_id: str) -> BackendUserContext:
        response = await self.client.get(
            f"{self.api_base_url}/api/v1/users/{user_id}",
            headers=self._headers()
        )
        response.raise_for_status()
        data = response.json()
        return BackendUserContext(**data)
    
    async def get_budget_info(self, user_id: str, project_id: str) -> BackendBudgetInfo:
        response = await self.client.get(
            f"{self.api_base_url}/api/v1/users/{user_id}/projects/{project_id}/budget",
            headers=self._headers()
        )
        response.raise_for_status()
        data = response.json()
        return BackendBudgetInfo(**data)
    
    async def get_policy_config(self, user_id: str, project_id: str) -> BackendPolicyConfig:
        response = await self.client.get(
            f"{self.api_base_url}/api/v1/users/{user_id}/projects/{project_id}/policies",
            headers=self._headers()
        )
        response.raise_for_status()
        data = response.json()
        return BackendPolicyConfig(**data)
    
    async def get_provider_cost(self, provider: str, model: str) -> BackendProviderCost:
        response = await self.client.get(
            f"{self.api_base_url}/api/v1/providers/{provider}/models/{model}/cost",
            headers=self._headers()
        )
        response.raise_for_status()
        data = response.json()
        return BackendProviderCost(**data)
    
    async def execute_payment(
        self,
        user_id: str,
        amount: float,
        metadata: dict
    ) -> BackendPaymentResult:
        response = await self.client.post(
            f"{self.api_base_url}/api/v1/payments/execute",
            headers=self._headers(),
            json={
                "user_id": user_id,
                "amount": amount,
                "currency": "USDC",
                "network": "arc",
                "metadata": metadata
            }
        )
        response.raise_for_status()
        data = response.json()
        return BackendPaymentResult(**data)
    
    async def get_payment_status(self, tx_hash: str) -> dict:
        response = await self.client.get(
            f"{self.api_base_url}/api/v1/payments/{tx_hash}/status",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    async def update_spending(
        self,
        user_id: str,
        project_id: str,
        amount: float,
        request_id: str
    ) -> bool:
        response = await self.client.post(
            f"{self.api_base_url}/api/v1/users/{user_id}/projects/{project_id}/spending",
            headers=self._headers(),
            json={
                "amount": amount,
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
        )
        response.raise_for_status()
        return response.json().get("success", False)
    
    async def store_audit_log(self, request_id: str, audit_data: dict) -> bool:
        response = await self.client.post(
            f"{self.api_base_url}/api/v1/audit/logs",
            headers=self._headers(),
            json={
                "request_id": request_id,
                "audit_data": audit_data,
                "timestamp": datetime.now().isoformat()
            }
        )
        response.raise_for_status()
        return response.json().get("success", False)
    
    async def call_provider_api(
        self,
        provider: str,
        endpoint: str,
        payload: dict
    ) -> dict:
        response = await self.client.post(
            f"{self.api_base_url}/api/v1/providers/{provider}/call",
            headers=self._headers(),
            json={
                "endpoint": endpoint,
                "payload": payload
            }
        )
        response.raise_for_status()
        return response.json()
```

---

## 🔌 Usage in Backend

```python
from integrations.backend_client import set_backend_client
from main import AgenticBrain

# Initialize
backend = ProductionBackendClient(
    api_base_url=os.environ["BACKEND_API_URL"],
    api_key=os.environ["BACKEND_API_KEY"]
)
set_backend_client(backend)

# Create brain
brain = AgenticBrain()

# Use in your API endpoint
@app.post("/api/process-request")
async def process_request(request_data: dict):
    result = await brain.process_request(request_data)
    return result
```

---

## ✅ Testing Checklist

- [ ] User service returns correct data
- [ ] Budget service tracks spending accurately
- [ ] Policy service enforces whitelists
- [ ] Payment service executes blockchain TXs
- [ ] Audit service stores logs correctly
- [ ] Provider gateway routes API calls
- [ ] Error handling for all endpoints
- [ ] Retry logic for transient failures
- [ ] Rate limiting configured
- [ ] Authentication working

---

## 🚨 Critical Requirements

1. **Arc Blockchain Integration**:
   - Must support USDC transfers
   - Must return transaction hash
   - Must track gas costs
   - Must handle confirmations

2. **Provider API Keys**:
   - Store securely (environment variables or secrets manager)
   - Rotate regularly
   - Never expose to frontend

3. **Audit Logs**:
   - Must persist all audit events
   - Must maintain hash chain integrity
   - Must support compliance queries

4. **Error Handling**:
   - Return clear error messages
   - Log all failures
   - Implement retry logic
   - Handle timeout gracefully

---

## 📚 Additional Resources

- **Complete Guide**: `PHASE_9_COMPLETE.md`
- **Full Example**: `src/example_production_backend.py`
- **Interface Definition**: `src/integrations/backend_client.py`
- **Architecture**: `PROJECT_SUMMARY.md`

---

## 💬 Questions?

Contact the AI/Brain team for:
- Interface clarifications
- Integration issues
- Architecture questions
- Testing support

---

**Quick Start**: Copy the template above and implement all 9 methods!
