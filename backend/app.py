"""
FastAPI application for SmartSpace backend API.
Refactored to use new modular architecture with FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from config import get_config
from src.container import get_container
from src.middleware.error_handler import register_error_handlers
from src.middleware.logging import register_logging_middleware
from src.routes.health import router as health_router
from src.routes.v1.chatbot import router as chatbot_v1_router
from src.routes.v1.requests import router as requests_v1_router
from src.routes.v1.text import router as text_v1_router
from src.routes.v1.audio import router as audio_v1_router
from src.routes.v1.images import router as images_v1_router
from src.routes.v1.embeddings import router as embeddings_v1_router
from src.routes.v1.vision import router as vision_v1_router
from src.routes.v1.models import router as models_v1_router
from src.services.chatbot import ChatbotService
from src.services.models.model_catalog_service import ModelCatalogService
from src.services.api_keys import ApiKeyService
from src.services.agentic import AgenticService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config=None):
    """
    Create and configure FastAPI application.
    
    Args:
        config: Optional configuration object
        
    Returns:
        Configured FastAPI app
    """
    if config is None:
        config = get_config()
    
    app = FastAPI(
        title="SmartSpace Backend API",
        description="Backend API for SmartSpace platform",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register middleware
    register_logging_middleware(app)
    register_error_handlers(app)
    
    # Register routes
    app.include_router(health_router)
    app.include_router(chatbot_v1_router, prefix="/api/v1", tags=["chatbot"])
    app.include_router(requests_v1_router, prefix="/api/v1", tags=["requests"])
    
    # Register facility-specific routes at root level (/v1/...)
    app.include_router(text_v1_router, prefix="/v1", tags=["text"])
    app.include_router(audio_v1_router, prefix="/v1", tags=["audio"])
    app.include_router(images_v1_router, prefix="/v1", tags=["images"])
    app.include_router(embeddings_v1_router, prefix="/v1", tags=["embeddings"])
    app.include_router(vision_v1_router, prefix="/v1", tags=["vision"])
    app.include_router(models_v1_router, prefix="/api/v1", tags=["models"])
    
    # Register services in container
    container = get_container()
    container.register(
        'chatbot_service',
        lambda c: ChatbotService(
            gemini_api_key=config.gemini_api_key,
            smartspace_doc_path=config.smartspace_doc_path
        ),
        singleton=True
    )
    container.register(
        'api_key_service',
        lambda c: ApiKeyService(),
        singleton=True
    )
    container.register(
        'agentic_service',
        lambda c: AgenticService(),
        singleton=True
    )
    container.register(
        'model_catalog_service',
        lambda c: ModelCatalogService(),
        singleton=True
    )
    
    logger.info("FastAPI application created successfully")
    
    return app


# Create app instance for direct execution
app = create_app()


if __name__ == '__main__':
    import uvicorn
    config = get_config()
    logger.info(f"Starting server on {config.host}:{config.port} (debug={config.debug})")
    uvicorn.run(
        "app:app",
        host=config.host,
        port=config.port,
        reload=config.debug,
        log_level="info"
    )
