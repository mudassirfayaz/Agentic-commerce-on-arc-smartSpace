"""Configuration settings for SmartSpace backend."""

from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    url: str = Field(default="postgresql://user:password@localhost:5432/smartspace", env="DATABASE_URL")
    pool_size: int = Field(default=10, env="DB_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DB_MAX_OVERFLOW")
    echo: bool = Field(default=False, env="DB_ECHO")
    
    class Config:
        env_prefix = "DB_"


class AgenticConfig(BaseSettings):
    """Agentic brain configuration."""
    enabled: bool = Field(default=True, env="AGENTIC_ENABLED")
    timeout: int = Field(default=30, env="AGENTIC_TIMEOUT")
    
    class Config:
        env_prefix = "AGENTIC_"


class PaymentConfig(BaseSettings):
    """Payment configuration."""
    arc_rpc_url: Optional[str] = Field(default=None, env="ARC_TESTNET_RPC_URL")
    usdc_contract_address: Optional[str] = Field(default=None, env="USDC_CONTRACT_ADDRESS")
    network: str = Field(default="arc_testnet", env="PAYMENT_NETWORK")
    
    class Config:
        env_prefix = "PAYMENT_"


class Config(BaseSettings):
    """Main configuration class."""
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    secret_key: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=5000, env="PORT")
    
    # Database
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # Agentic Brain
    agentic: AgenticConfig = Field(default_factory=AgenticConfig)
    
    # Payment
    payment: PaymentConfig = Field(default_factory=PaymentConfig)
    
    # Chatbot
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    smartspace_doc_path: Optional[str] = Field(
        default=None,
        env="SMARTSPACE_DOC_PATH"
    )
    
    # CORS
    cors_origins: List[str] = Field(
        default_factory=lambda: ["*"],
        env="CORS_ORIGINS"
    )
    
    def __init__(self, **kwargs):
        """Initialize configuration."""
        super().__init__(**kwargs)
        
        # Set default smartspace doc path if not provided
        if self.smartspace_doc_path is None:
            import os
            from pathlib import Path
            self.smartspace_doc_path = str(
                Path(__file__).parent.parent.parent / "openspec" / "SmartSpace.md"
            )
        
        # Parse CORS origins if string
        if isinstance(self.cors_origins, str):
            self.cors_origins = self.cors_origins.split(",") if self.cors_origins != "*" else ["*"]
        
        # Set debug based on environment
        if self.debug is None:
            self.debug = self.environment == "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


_config_instance: Optional[Config] = None


def get_config() -> Config:
    """Get the configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
