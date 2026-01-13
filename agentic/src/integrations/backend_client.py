"""
Backend integration interfaces for SmartSpace Agentic Brain.

This module defines the interfaces the brain expects from the backend.
Backend team should implement these interfaces to enable full integration.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BackendUserContext:
    """User context data from backend"""
    user_id: str
    project_id: str
    account_status: str  # "active", "suspended", "trial"
    tier: str  # "free", "pro", "enterprise"
    created_at: datetime
    total_spending: float
    request_count: int
    metadata: Dict[str, Any]


@dataclass
class BackendBudgetInfo:
    """Budget information from backend"""
    user_id: str
    project_id: str
    daily_limit: float
    monthly_limit: float
    per_request_limit: float
    current_daily_spending: float
    current_monthly_spending: float
    available_balance: float
    currency: str = "USDC"


@dataclass
class BackendPolicyConfig:
    """Policy configuration from backend"""
    user_id: str
    project_id: str
    allowed_providers: List[str]
    allowed_models: Dict[str, List[str]]
    rate_limit_per_minute: int
    rate_limit_per_hour: int
    forbidden_operations: List[str]
    require_approval_above: float  # Cost threshold for manual approval
    metadata: Dict[str, Any]


@dataclass
class BackendPaymentResult:
    """Payment result from backend blockchain integration"""
    success: bool
    tx_hash: str
    block_number: Optional[int]
    amount: float
    currency: str
    from_address: str
    to_address: str
    gas_used: Optional[float]
    timestamp: datetime
    error: Optional[str] = None


@dataclass
class BackendProviderCost:
    """Real-time cost from provider"""
    provider: str
    model: str
    cost_per_1k_input_tokens: float
    cost_per_1k_output_tokens: float
    cost_per_request: float
    last_updated: datetime


class BackendClient(ABC):
    """
    Abstract interface for backend integration.
    
    Backend team should implement this interface to connect the
    agentic brain with the SmartSpace backend services.
    """
    
    @abstractmethod
    async def get_user_context(
        self,
        user_id: str,
        project_id: str
    ) -> BackendUserContext:
        """
        Fetch user context from backend database.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            BackendUserContext with user details
            
        Raises:
            UserNotFoundException: If user doesn't exist
            ProjectNotFoundException: If project doesn't exist
        """
        pass
    
    @abstractmethod
    async def get_budget_info(
        self,
        user_id: str,
        project_id: str
    ) -> BackendBudgetInfo:
        """
        Fetch current budget information from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            BackendBudgetInfo with current spending and limits
        """
        pass
    
    @abstractmethod
    async def get_policy_config(
        self,
        user_id: str,
        project_id: str
    ) -> BackendPolicyConfig:
        """
        Fetch user's policy configuration from backend.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            
        Returns:
            BackendPolicyConfig with allowed providers, models, and limits
        """
        pass
    
    @abstractmethod
    async def get_provider_cost(
        self,
        provider: str,
        model: str
    ) -> BackendProviderCost:
        """
        Get real-time cost information for a provider/model.
        
        Args:
            provider: Provider name (e.g., "openai")
            model: Model name (e.g., "gpt-4")
            
        Returns:
            BackendProviderCost with current pricing
        """
        pass
    
    @abstractmethod
    async def execute_payment(
        self,
        user_id: str,
        project_id: str,
        amount: float,
        request_id: str,
        metadata: Dict[str, Any]
    ) -> BackendPaymentResult:
        """
        Execute payment via blockchain (Arc + Circle USDC).
        
        This method should:
        1. Verify user has sufficient USDC balance
        2. Execute blockchain transaction on Arc network
        3. Wait for transaction confirmation
        4. Return transaction details
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            amount: Amount in USDC to pay
            request_id: Request identifier for tracking
            metadata: Additional payment metadata
            
        Returns:
            BackendPaymentResult with transaction details
            
        Raises:
            InsufficientBalanceError: If user doesn't have enough USDC
            PaymentExecutionError: If blockchain transaction fails
        """
        pass
    
    @abstractmethod
    async def get_payment_status(
        self,
        tx_hash: str
    ) -> Dict[str, Any]:
        """
        Query payment status from blockchain.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Dict with payment status details
        """
        pass
    
    @abstractmethod
    async def update_spending(
        self,
        user_id: str,
        project_id: str,
        amount: float,
        request_id: str
    ) -> None:
        """
        Update user's spending records in backend database.
        
        Args:
            user_id: User identifier
            project_id: Project identifier
            amount: Amount spent
            request_id: Request identifier
        """
        pass
    
    @abstractmethod
    async def store_audit_log(
        self,
        request_id: str,
        audit_data: Dict[str, Any]
    ) -> None:
        """
        Store audit log in backend database.
        
        Args:
            request_id: Request identifier
            audit_data: Complete audit trail
        """
        pass
    
    @abstractmethod
    async def call_provider_api(
        self,
        provider: str,
        model: str,
        endpoint: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call provider API through backend gateway.
        
        Backend should:
        1. Route request to appropriate provider (OpenAI, Anthropic, etc.)
        2. Include backend's API keys (not exposed to brain)
        3. Parse response
        4. Calculate actual cost
        5. Return standardized response
        
        Args:
            provider: Provider name
            model: Model name
            endpoint: API endpoint
            parameters: Request parameters
            
        Returns:
            Dict with response data, cost, and tokens used
        """
        pass


class MockBackendClient(BackendClient):
    """
    Mock implementation for development and testing.
    
    This provides realistic responses without requiring
    actual backend services.
    """
    
    async def get_user_context(
        self,
        user_id: str,
        project_id: str
    ) -> BackendUserContext:
        """Return mock user context"""
        return BackendUserContext(
            user_id=user_id,
            project_id=project_id,
            account_status="active",
            tier="pro",
            created_at=datetime.utcnow(),
            total_spending=125.50,
            request_count=1250,
            metadata={"plan": "monthly"}
        )
    
    async def get_budget_info(
        self,
        user_id: str,
        project_id: str
    ) -> BackendBudgetInfo:
        """Return mock budget info"""
        return BackendBudgetInfo(
            user_id=user_id,
            project_id=project_id,
            daily_limit=100.0,
            monthly_limit=1000.0,
            per_request_limit=10.0,
            current_daily_spending=5.25,
            current_monthly_spending=125.50,
            available_balance=874.50,
            currency="USDC"
        )
    
    async def get_policy_config(
        self,
        user_id: str,
        project_id: str
    ) -> BackendPolicyConfig:
        """Return mock policy config"""
        return BackendPolicyConfig(
            user_id=user_id,
            project_id=project_id,
            allowed_providers=["openai", "anthropic", "google"],
            allowed_models={
                "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-vision"],
                "anthropic": ["claude-3-opus", "claude-3-sonnet"],
                "google": ["gemini-pro", "gemini-pro-vision"]
            },
            rate_limit_per_minute=60,
            rate_limit_per_hour=1000,
            forbidden_operations=[],
            require_approval_above=50.0,
            metadata={}
        )
    
    async def get_provider_cost(
        self,
        provider: str,
        model: str
    ) -> BackendProviderCost:
        """Return mock provider cost"""
        costs = {
            ("openai", "gpt-4"): (0.03, 0.06, 0.0),
            ("openai", "gpt-3.5-turbo"): (0.001, 0.002, 0.0),
            ("anthropic", "claude-3-opus"): (0.015, 0.075, 0.0),
            ("google", "gemini-pro"): (0.00025, 0.0005, 0.0),
        }
        
        cost_data = costs.get((provider, model), (0.01, 0.02, 0.0))
        
        return BackendProviderCost(
            provider=provider,
            model=model,
            cost_per_1k_input_tokens=cost_data[0],
            cost_per_1k_output_tokens=cost_data[1],
            cost_per_request=cost_data[2],
            last_updated=datetime.utcnow()
        )
    
    async def execute_payment(
        self,
        user_id: str,
        project_id: str,
        amount: float,
        request_id: str,
        metadata: Dict[str, Any]
    ) -> BackendPaymentResult:
        """Return mock payment result"""
        import hashlib
        import time
        
        # Generate mock tx hash
        tx_data = f"{user_id}{project_id}{amount}{time.time()}"
        tx_hash = "0x" + hashlib.sha256(tx_data.encode()).hexdigest()[:40]
        
        return BackendPaymentResult(
            success=True,
            tx_hash=tx_hash,
            block_number=12345678,
            amount=amount,
            currency="USDC",
            from_address="0xuser_wallet_address",
            to_address="0xsmartspace_wallet",
            gas_used=0.0001,
            timestamp=datetime.utcnow()
        )
    
    async def get_payment_status(
        self,
        tx_hash: str
    ) -> Dict[str, Any]:
        """Return mock payment status"""
        return {
            "status": "confirmed",
            "confirmations": 12,
            "tx_hash": tx_hash,
            "success": True
        }
    
    async def update_spending(
        self,
        user_id: str,
        project_id: str,
        amount: float,
        request_id: str
    ) -> None:
        """Mock spending update"""
        # In real implementation, update database
        pass
    
    async def store_audit_log(
        self,
        request_id: str,
        audit_data: Dict[str, Any]
    ) -> None:
        """Mock audit log storage"""
        # In real implementation, store in database
        pass
    
    async def call_provider_api(
        self,
        provider: str,
        model: str,
        endpoint: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Return mock API response"""
        return {
            'data': {
                'message': f'Mock response from {provider}/{model}',
                'content': 'This is a simulated API response for testing.',
                'model': model
            },
            'cost': 0.002,
            'tokens': {
                'input': 50,
                'output': 100,
                'total': 150
            },
            'usage': {
                'prompt_tokens': 50,
                'completion_tokens': 100,
                'total_tokens': 150
            }
        }


# Singleton instance for easy access
_backend_client: Optional[BackendClient] = None


def get_backend_client() -> BackendClient:
    """
    Get the backend client instance.
    
    Returns mock client by default. Backend team should replace
    with real implementation.
    """
    global _backend_client
    if _backend_client is None:
        _backend_client = MockBackendClient()
    return _backend_client


def set_backend_client(client: BackendClient) -> None:
    """
    Set the backend client implementation.
    
    Backend team should call this during initialization to inject
    their real implementation.
    """
    global _backend_client
    _backend_client = client
