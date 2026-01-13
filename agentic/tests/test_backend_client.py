"""
Tests for BackendClient module
"""

import pytest
from datetime import datetime

from integrations.backend_client import (
    BackendClient,
    MockBackendClient,
    BackendUserContext,
    BackendBudgetInfo,
    BackendPolicyConfig,
    BackendPaymentResult,
    BackendProviderCost
)


@pytest.fixture
def mock_client():
    """Create MockBackendClient instance"""
    return MockBackendClient()


class TestBackendUserContext:
    """Test BackendUserContext dataclass"""
    
    def test_user_context_creation(self):
        """Test creating user context"""
        context = BackendUserContext(
            user_id="user_001",
            project_id="proj_001",
            account_status="active",
            tier="pro",
            created_at=datetime.utcnow(),
            total_spending=100.0,
            request_count=500,
            metadata={"plan": "monthly"}
        )
        
        assert context.user_id == "user_001"
        assert context.project_id == "proj_001"
        assert context.account_status == "active"
        assert context.tier == "pro"
        assert context.total_spending == 100.0
        assert context.request_count == 500


class TestBackendBudgetInfo:
    """Test BackendBudgetInfo dataclass"""
    
    def test_budget_info_creation(self):
        """Test creating budget info"""
        budget = BackendBudgetInfo(
            user_id="user_001",
            project_id="proj_001",
            daily_limit=100.0,
            monthly_limit=1000.0,
            per_request_limit=10.0,
            current_daily_spending=5.0,
            current_monthly_spending=125.0,
            available_balance=875.0,
            currency="USDC"
        )
        
        assert budget.daily_limit == 100.0
        assert budget.monthly_limit == 1000.0
        assert budget.available_balance == 875.0
        assert budget.currency == "USDC"


class TestBackendPolicyConfig:
    """Test BackendPolicyConfig dataclass"""
    
    def test_policy_config_creation(self):
        """Test creating policy config"""
        policy = BackendPolicyConfig(
            user_id="user_001",
            project_id="proj_001",
            allowed_providers=["openai", "anthropic"],
            allowed_models={
                "openai": ["gpt-4", "gpt-3.5-turbo"],
                "anthropic": ["claude-3-opus"]
            },
            rate_limit_per_minute=60,
            rate_limit_per_hour=1000,
            forbidden_operations=["image_generation"],
            require_approval_above=50.0,
            metadata={"version": "1.0"}
        )
        
        assert "openai" in policy.allowed_providers
        assert "anthropic" in policy.allowed_providers
        assert policy.rate_limit_per_minute == 60
        assert policy.require_approval_above == 50.0


class TestBackendPaymentResult:
    """Test BackendPaymentResult dataclass"""
    
    def test_payment_result_creation(self):
        """Test creating payment result"""
        payment = BackendPaymentResult(
            success=True,
            tx_hash="0xabc123",
            block_number=12345678,
            amount=5.0,
            currency="USDC",
            from_address="0xuser",
            to_address="0xplatform",
            gas_used=0.0001,
            timestamp=datetime.utcnow()
        )
        
        assert payment.success is True
        assert payment.tx_hash == "0xabc123"
        assert payment.amount == 5.0
        assert payment.currency == "USDC"


class TestBackendProviderCost:
    """Test BackendProviderCost dataclass"""
    
    def test_provider_cost_creation(self):
        """Test creating provider cost"""
        cost = BackendProviderCost(
            provider="openai",
            model="gpt-4",
            cost_per_1k_input_tokens=0.03,
            cost_per_1k_output_tokens=0.06,
            cost_per_request=0.0,
            last_updated=datetime.utcnow()
        )
        
        assert cost.provider == "openai"
        assert cost.model == "gpt-4"
        assert cost.cost_per_1k_input_tokens == 0.03
        assert cost.cost_per_1k_output_tokens == 0.06


class TestMockBackendClient:
    """Test MockBackendClient implementation"""
    
    @pytest.mark.asyncio
    async def test_get_user_context(self, mock_client):
        """Test getting user context"""
        context = await mock_client.get_user_context(
            user_id="user_001",
            project_id="proj_001"
        )
        
        assert isinstance(context, BackendUserContext)
        assert context.user_id == "user_001"
        assert context.project_id == "proj_001"
        assert context.account_status == "active"
        assert context.tier == "pro"
        assert context.total_spending > 0
        assert context.request_count > 0
    
    @pytest.mark.asyncio
    async def test_get_budget_info(self, mock_client):
        """Test getting budget info"""
        budget = await mock_client.get_budget_info(
            user_id="user_001",
            project_id="proj_001"
        )
        
        assert isinstance(budget, BackendBudgetInfo)
        assert budget.user_id == "user_001"
        assert budget.project_id == "proj_001"
        assert budget.daily_limit > 0
        assert budget.monthly_limit > 0
        assert budget.currency == "USDC"
        assert budget.available_balance >= 0
    
    @pytest.mark.asyncio
    async def test_get_policy_config(self, mock_client):
        """Test getting policy config"""
        policy = await mock_client.get_policy_config(
            user_id="user_001",
            project_id="proj_001"
        )
        
        assert isinstance(policy, BackendPolicyConfig)
        assert policy.user_id == "user_001"
        assert policy.project_id == "proj_001"
        assert len(policy.allowed_providers) > 0
        assert len(policy.allowed_models) > 0
        assert policy.rate_limit_per_minute > 0
        assert policy.rate_limit_per_hour > 0
    
    @pytest.mark.asyncio
    async def test_get_provider_cost(self, mock_client):
        """Test getting provider cost"""
        cost = await mock_client.get_provider_cost(
            provider="openai",
            model="gpt-4"
        )
        
        assert isinstance(cost, BackendProviderCost)
        assert cost.provider == "openai"
        assert cost.model == "gpt-4"
        assert cost.cost_per_1k_input_tokens > 0
        assert cost.cost_per_1k_output_tokens > 0
        assert cost.last_updated is not None
    
    @pytest.mark.asyncio
    async def test_execute_payment(self, mock_client):
        """Test executing payment"""
        payment = await mock_client.execute_payment(
            user_id="user_001",
            project_id="proj_001",
            amount=5.0,
            request_id="req_001",
            metadata={"test": "data"}
        )
        
        assert isinstance(payment, BackendPaymentResult)
        assert payment.success is True
        assert payment.amount == 5.0
        assert payment.currency == "USDC"
        assert payment.tx_hash.startswith("0x")
        assert len(payment.tx_hash) > 10
        assert payment.block_number > 0
        assert payment.from_address is not None
        assert payment.to_address is not None
    
    @pytest.mark.asyncio
    async def test_get_payment_status(self, mock_client):
        """Test getting payment status"""
        status = await mock_client.get_payment_status(
            tx_hash="0xabc123"
        )
        
        assert isinstance(status, dict)
        assert "status" in status
        assert status["status"] in ["pending", "confirmed", "failed"]
    
    @pytest.mark.asyncio
    async def test_update_spending(self, mock_client):
        """Test updating spending"""
        # Should not raise exception
        await mock_client.update_spending(
            user_id="user_001",
            project_id="proj_001",
            amount=5.0,
            request_id="req_001"
        )
    
    @pytest.mark.asyncio
    async def test_store_audit_log(self, mock_client):
        """Test storing audit log"""
        # Should not raise exception
        await mock_client.store_audit_log(
            request_id="req_001",
            audit_data={"test": "data"}
        )
    
    @pytest.mark.asyncio
    async def test_call_provider_api(self, mock_client):
        """Test calling provider API"""
        response = await mock_client.call_provider_api(
            provider="openai",
            model="gpt-4",
            endpoint="/chat/completions",
            parameters={
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 100
            }
        )
        
        assert isinstance(response, dict)
        assert "data" in response or "response" in response
        assert "cost" in response
        assert "tokens" in response or "tokens_used" in response


class TestProviderCosts:
    """Test provider cost retrieval for multiple providers"""
    
    @pytest.mark.asyncio
    async def test_openai_gpt4_cost(self, mock_client):
        """Test OpenAI GPT-4 cost"""
        cost = await mock_client.get_provider_cost("openai", "gpt-4")
        assert cost.cost_per_1k_input_tokens == 0.03
        assert cost.cost_per_1k_output_tokens == 0.06
    
    @pytest.mark.asyncio
    async def test_openai_gpt35_cost(self, mock_client):
        """Test OpenAI GPT-3.5 cost"""
        cost = await mock_client.get_provider_cost("openai", "gpt-3.5-turbo")
        assert cost.cost_per_1k_input_tokens == 0.001
        assert cost.cost_per_1k_output_tokens == 0.002
    
    @pytest.mark.asyncio
    async def test_anthropic_opus_cost(self, mock_client):
        """Test Anthropic Claude cost"""
        cost = await mock_client.get_provider_cost("anthropic", "claude-3-opus")
        assert cost.cost_per_1k_input_tokens == 0.015
        assert cost.cost_per_1k_output_tokens == 0.075
    
    @pytest.mark.asyncio
    async def test_google_gemini_cost(self, mock_client):
        """Test Google Gemini cost"""
        cost = await mock_client.get_provider_cost("google", "gemini-pro")
        assert cost.cost_per_1k_input_tokens == 0.00025
        assert cost.cost_per_1k_output_tokens == 0.0005
    
    @pytest.mark.asyncio
    async def test_unknown_provider_cost(self, mock_client):
        """Test unknown provider returns default cost"""
        cost = await mock_client.get_provider_cost("unknown", "unknown-model")
        assert cost.cost_per_1k_input_tokens == 0.01
        assert cost.cost_per_1k_output_tokens == 0.02


class TestBudgetCalculations:
    """Test budget-related calculations"""
    
    @pytest.mark.asyncio
    async def test_available_budget_calculation(self, mock_client):
        """Test available budget is correctly calculated"""
        budget = await mock_client.get_budget_info("user_001", "proj_001")
        
        # available_balance should equal monthly_limit - current_monthly_spending
        expected_available = budget.monthly_limit - budget.current_monthly_spending
        assert budget.available_balance == expected_available
    
    @pytest.mark.asyncio
    async def test_daily_spending_within_limit(self, mock_client):
        """Test daily spending is within daily limit"""
        budget = await mock_client.get_budget_info("user_001", "proj_001")
        assert budget.current_daily_spending < budget.daily_limit
    
    @pytest.mark.asyncio
    async def test_monthly_spending_within_limit(self, mock_client):
        """Test monthly spending is within monthly limit"""
        budget = await mock_client.get_budget_info("user_001", "proj_001")
        assert budget.current_monthly_spending < budget.monthly_limit


class TestPolicyValidation:
    """Test policy configuration validation"""
    
    @pytest.mark.asyncio
    async def test_allowed_providers_not_empty(self, mock_client):
        """Test allowed providers list is not empty"""
        policy = await mock_client.get_policy_config("user_001", "proj_001")
        assert len(policy.allowed_providers) > 0
    
    @pytest.mark.asyncio
    async def test_allowed_models_not_empty(self, mock_client):
        """Test allowed models dict is not empty"""
        policy = await mock_client.get_policy_config("user_001", "proj_001")
        assert len(policy.allowed_models) > 0
    
    @pytest.mark.asyncio
    async def test_rate_limits_are_positive(self, mock_client):
        """Test rate limits are positive numbers"""
        policy = await mock_client.get_policy_config("user_001", "proj_001")
        assert policy.rate_limit_per_minute > 0
        assert policy.rate_limit_per_hour > 0
    
    @pytest.mark.asyncio
    async def test_approval_threshold_is_positive(self, mock_client):
        """Test approval threshold is positive"""
        policy = await mock_client.get_policy_config("user_001", "proj_001")
        assert policy.require_approval_above > 0
