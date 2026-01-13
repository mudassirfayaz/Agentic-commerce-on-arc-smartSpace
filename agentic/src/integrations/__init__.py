"""
Integration module for SmartSpace Agentic Brain.

Provides interfaces for backend integration.
"""

from .backend_client import (
    BackendClient,
    MockBackendClient,
    BackendUserContext,
    BackendBudgetInfo,
    BackendPolicyConfig,
    BackendPaymentResult,
    BackendProviderCost,
    get_backend_client,
    set_backend_client
)

__all__ = [
    'BackendClient',
    'MockBackendClient',
    'BackendUserContext',
    'BackendBudgetInfo',
    'BackendPolicyConfig',
    'BackendPaymentResult',
    'BackendProviderCost',
    'get_backend_client',
    'set_backend_client'
]
