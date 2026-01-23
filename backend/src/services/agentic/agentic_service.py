"""
Agentic brain integration service.
Wraps the agentic brain module for use in the backend.
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Add agentic directory to path
agentic_path = Path(__file__).parent.parent.parent.parent / "agentic"
if str(agentic_path) not in sys.path:
    sys.path.insert(0, str(agentic_path))


class AgenticService:
    """Service for integrating with the agentic brain."""
    
    def __init__(self):
        """Initialize agentic service."""
        self.brain = None
        self._initialize_brain()
    
    def _initialize_brain(self):
        """Initialize the agentic brain."""
        try:
            # Import agentic brain
            from agentic.src.main import AgenticBrain
            self.brain = AgenticBrain()
            logger.info("Agentic brain initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agentic brain: {e}")
            self.brain = None
    
    async def process_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request through the agentic brain.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Processing result from agentic brain
        """
        if not self.brain:
            raise RuntimeError("Agentic brain not initialized")
        
        try:
            result = await self.brain.process_request(request_data)
            return result
        except Exception as e:
            logger.error(f"Error processing request in agentic brain: {e}")
            raise

