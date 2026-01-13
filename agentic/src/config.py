"""
Configuration for Agentic System

Defines API endpoints and configuration for backend communication.
"""

import os
from typing import Dict, Any


class Config:
    """Configuration settings for the agentic system"""
    
    # Backend API Configuration
    BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:5000/api")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # seconds
    
    # API Endpoints
    ENDPOINTS = {
        # User endpoints
        "users": {
            "get_user": "/users/{user_id}",
            "get_context": "/users/{user_id}/context",
            "update_user": "/users/{user_id}",
        },
        
        # Policy endpoints
        "policies": {
            "get_policy": "/policies/{user_id}/{project_id}",
            "update_policy": "/policies/{user_id}/{project_id}",
            "validate_provider": "/policies/{user_id}/{project_id}/validate-provider",
            "validate_model": "/policies/{user_id}/{project_id}/validate-model",
        },
        
        # Budget endpoints - Now directly accessible as base URL
        "budgets": "/budgets",
        
        # Pricing endpoints - Now directly accessible as base URL
        "pricing": "/pricing",
        
        # Request endpoints
        "requests": {
            "create_request": "/requests",
            "get_request": "/requests/{request_id}",
            "update_request": "/requests/{request_id}",
            "get_user_requests": "/requests/user/{user_id}",
        },
        
        # Audit endpoints
        "audits": {
            "create_log": "/audits",
            "add_entry": "/audits/{audit_id}/entries",
            "get_log": "/audits/{audit_id}",
            "get_request_logs": "/audits/request/{request_id}",
        },
        
        # Risk endpoints
        "risk": {
            "get_baseline": "/risk/baseline/{user_id}/{project_id}",
            "update_baseline": "/risk/baseline/{user_id}/{project_id}",
            "assess_risk": "/risk/assess",
            "get_assessment": "/risk/assessment/{assessment_id}",
        },
        
        # Decision endpoints
        "decisions": {
            "create_decision": "/decisions",
            "get_decision": "/decisions/{decision_id}",
            "get_request_decision": "/decisions/request/{request_id}",
        },
        
        # Cost endpoints (legacy - use 'pricing' instead)
        "costs": {
            "get_pricing": "/costs/pricing/{provider}/{model}",
            "estimate_cost": "/costs/estimate",
            "compare_costs": "/costs/compare",
        }
    }
    
    # Agent Configuration
    AGENT_TIERS = {
        "FLASH": {
            "max_risk_score": 5.0,
            "max_cost": 0.01,
            "auto_approve": True,
        },
        "PRO": {
            "max_risk_score": 8.0,
            "max_cost": 1.0,
            "auto_approve": False,
        }
    }
    
    # Default values
    DEFAULTS = {
        "per_request_limit": 10.0,
        "daily_budget": 100.0,
        "monthly_budget": 3000.0,
        "rate_limit_per_minute": 10,
        "rate_limit_per_hour": 100,
        "max_risk_score": 7.0,
        "auto_approve_risk_threshold": 3.0,
    }
    
    @classmethod
    def get_endpoint(cls, category: str, endpoint_name: str = None, **kwargs) -> str:
        """
        Get full URL for an endpoint with parameters filled in.
        
        Args:
            category: Endpoint category (e.g., 'users', 'policies', 'budgets', 'pricing')
            endpoint_name: Specific endpoint name (optional for base URL categories)
            **kwargs: Parameters to fill in URL template
            
        Returns:
            Full URL string
            
        Examples:
            # Dictionary-based endpoint
            url = Config.get_endpoint('policies', 'get_policy', 
                                     user_id='user_001', project_id='proj_001')
            
            # String-based base URL endpoint
            url = Config.get_endpoint('budgets')  # Returns base budgets URL
            url = Config.get_endpoint('pricing')  # Returns base pricing URL
        """
        endpoint = cls.ENDPOINTS.get(category)
        
        # Handle string-based endpoints (direct URLs)
        if isinstance(endpoint, str):
            return f"{cls.BACKEND_API_URL}{endpoint}"
        
        # Handle dictionary-based endpoints
        if endpoint_name is None:
            raise ValueError(f"endpoint_name required for category '{category}'")
        
        endpoint_path = endpoint[endpoint_name]
        
        # Fill in URL parameters
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            endpoint_path = endpoint_path.replace(placeholder, str(value))
        
        return f"{cls.BACKEND_API_URL}{endpoint_path}"
    
    @classmethod
    def get_all_endpoints(cls) -> Dict[str, Any]:
        """Get all configured endpoints"""
        return cls.ENDPOINTS


# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:5000/api")


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    BACKEND_API_URL = os.getenv("BACKEND_API_URL", "https://api.smartspace.arc/api")
    API_TIMEOUT = 60


class TestConfig(Config):
    """Test environment configuration"""
    DEBUG = True
    BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:5001/api")
    API_TIMEOUT = 10


# Select configuration based on environment
ENV = os.getenv("ENVIRONMENT", "development").lower()

if ENV == "production":
    config = ProductionConfig()
elif ENV == "test":
    config = TestConfig()
else:
    config = DevelopmentConfig()
