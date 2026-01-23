"""
SmartSpace Agentic Brain - Main Orchestrator

Request Flow:
1. Frontend/User → Backend API (receives request)
2. Backend → Agentic Brain (forwards for processing)
3. Brain delegates to Decision Engine:
   - Validate request structure
   - Load user context & policies
   - Validate provider/model whitelist
   - Estimate costs
   - Check budget availability
   - Validate against policies
   - Assess risk
   - Route to appropriate agent tier
   - Get AI decision
   - Log everything
4. Brain executes approved requests:
   - Pay estimated amount (blockchain TX)
   - Call provider API
   - Log cost variance
5. Brain → Backend (returns response + updates state)
6. Backend → Frontend/User (final response)

The brain now uses a dedicated Decision Engine for all decision logic,
keeping the orchestrator focused on execution and coordination.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from config import Config
from models.request import APIRequest
from models.decision import Decision, DecisionOutcome
from decision_engine.decision_engine import AutonomousPaymentDecisionEngine
from payments.payment_executor import PaymentExecutor, PaymentReservation, PaymentResult
from audit_logging.audit_logger import AuditLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgenticBrain:
    """
    The SmartSpace Agentic Brain - Main orchestrator for API requests.
    
    This orchestrator:
    1. Receives requests from backend
    2. Delegates decision making to the Decision Engine
    3. Executes approved requests (payment + API call)
    4. Returns results to backend
    
    The heavy lifting of decision logic is handled by the
    Autonomous Payment Decision Engine.
    """
    
    def __init__(self):
        """Initialize the agentic brain with decision engine."""
        self.config = Config()
        self.decision_engine = AutonomousPaymentDecisionEngine()
        self.payment_executor = PaymentExecutor()
        self.audit_logger = AuditLogger(log_dir="audit_logs")
        
        logger.info("🧠 Agentic Brain initialized with Decision Engine")
    
    async def process_request(
        self,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process an API request through the complete flow.
        
        This simplified orchestrator:
        1. Creates APIRequest object from request_data
        2. Delegates decision making to Decision Engine
        3. Executes approved requests (payment + API call)
        4. Returns complete response with decision and execution results
        
        Args:
            request_data: Dictionary with request details from backend
                
        Returns:
            Dictionary with result:
                - success: bool
                - decision: Decision object dict
                - response: API response (if executed)
                - payment: Payment details (if executed)
                - message: Human-readable message
        """
        start_time = datetime.utcnow()
        
        try:
            logger.info(f"📥 Processing request from user {request_data.get('user_id')}")
            
            # Create APIRequest object
            api_request = await self._create_request_from_data(request_data)
            
            # Log request received
            await self.audit_logger.log_request_received(
                request_id=api_request.request_id,
                user_id=api_request.user_id,
                project_id=api_request.project_id,
                agent_id=api_request.agent_id,
                request_details={
                    'provider': api_request.api_provider,
                    'model': api_request.model_name,
                    'endpoint': api_request.endpoint,
                    'estimated_tokens': api_request.estimated_tokens,
                    'source': request_data.get('request_source', 'user')
                }
            )
            
            # Delegate to Decision Engine for complete decision logic
            logger.info("🧠 Delegating to Decision Engine...")
            decision = await self.decision_engine.process_request(api_request)
            
            # If approved, execute the request
            if decision.outcome == DecisionOutcome.APPROVED:
                logger.info("✅ Request approved! Executing payment and API call...")
                
                # Execute payment + API call + log variance
                response, payment_result = await self._execute_approved_request(
                    api_request,
                    decision
                )
                
                # Log completion
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.info(
                    f"✅ Request completed in {duration:.2f}s | "
                    f"Paid: ${payment_result.estimated_amount:.4f} USDC | "
                    f"Actual: ${payment_result.actual_amount:.4f} | "
                    f"Variance: ${payment_result.variance_amount:+.4f} ({payment_result.variance_percent:+.1f}%)"
                )
                
                return {
                    'success': True,
                    'decision': decision.to_dict(),
                    'response': response,
                    'payment': payment_result.to_dict(),
                    'message': 'Request approved and executed successfully'
                }
            else:
                logger.info(f"❌ Request {decision.outcome.value}: {decision.rejection_reason}")
                
                return {
                    'success': False,
                    'decision': decision.to_dict(),
                    'response': None,
                    'payment': None,
                    'message': decision.rejection_reason or decision.reasoning
                }
                
        except Exception as e:
            logger.error(f"❌ Error processing request: {e}", exc_info=True)
            
            # Log error
            if 'api_request' in locals():
                await self.audit_logger.log_error(
                    request_id=api_request.request_id,
                    user_id=api_request.user_id,
                    project_id=api_request.project_id,
                    error=str(e),
                    error_details={'exception_type': type(e).__name__}
                )
            
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing request'
            }
    
    async def _create_request_from_data(
        self,
        request_data: Dict[str, Any]
    ) -> APIRequest:
        """
        Create APIRequest object from request data dictionary.
        
        Args:
            request_data: Request data from backend
            
        Returns:
            APIRequest object
        """
        request_id = request_data.get('request_id') or f"req_{uuid.uuid4().hex[:12]}"
        
        return APIRequest(
            request_id=request_id,
            user_id=request_data['user_id'],
            project_id=request_data['project_id'],
            agent_id=request_data.get('agent_id'),
            api_provider=request_data['api_provider'],
            model_name=request_data['model_name'],
            endpoint=request_data.get('endpoint', '/chat/completions'),
            parameters=request_data.get('parameters', {}),
            estimated_tokens=request_data.get('estimated_tokens', 1000),
            timestamp=datetime.utcnow()
        )
    
    async def _execute_approved_request(
        self,
        api_request: APIRequest,
        decision: Decision
    ) -> Tuple[Dict[str, Any], PaymentResult]:
        """
        Execute an approved request: payment + API call + variance logging.
        
        Args:
            api_request: The approved API request
            decision: The approval decision
            
        Returns:
            Tuple of (api_response, payment_result)
        """
        # Step 1: Pay estimated amount (single blockchain TX)
        logger.info("💰 Step 1: Paying estimated amount...")
        payment_reservation = await self.payment_executor.reserve_payment(
            request_id=api_request.request_id,
            user_id=api_request.user_id,
            project_id=api_request.project_id,
            estimated_amount=api_request.estimated_cost
        )
        
        # Log payment to audit system
        await self.audit_logger.log_payment_reserved(
            request_id=api_request.request_id,
            user_id=api_request.user_id,
            project_id=api_request.project_id,
            amount=payment_reservation.estimated_amount,
            tx_hash=payment_reservation.tx_hash,
            reservation_id=payment_reservation.reservation_id
        )
        
        # Step 2: Execute API call
        logger.info("🚀 Step 2: Executing API call...")
        api_response = await self._call_provider_api(api_request)
        
        # Extract actual cost from response
        api_request.actual_cost = api_response.get('cost', api_request.estimated_cost)
        
        # Log API call success
        await self.audit_logger.log_api_call_success(
            request_id=api_request.request_id,
            user_id=api_request.user_id,
            project_id=api_request.project_id,
            provider=api_request.api_provider,
            model=api_request.model_name,
            actual_cost=api_request.actual_cost,
            response_details={
                'tokens': api_response.get('tokens', api_request.estimated_tokens),
                'status': 'success'
            }
        )
        
        # Step 3: Log cost variance
        logger.info("📊 Step 3: Logging cost variance...")
        payment_result = await self.payment_executor.commit_payment(
            reservation=payment_reservation,
            actual_amount=api_request.actual_cost,
            provider=api_request.api_provider
        )
        
        # Log payment completion
        await self.audit_logger.log_payment_completed(
            request_id=api_request.request_id,
            user_id=api_request.user_id,
            project_id=api_request.project_id,
            estimated_amount=payment_result.estimated_amount,
            actual_amount=payment_result.actual_amount,
            variance=payment_result.variance_amount
        )
        
        return api_response, payment_result
    
    async def _call_provider_api(
        self,
        api_request: APIRequest
    ) -> Dict[str, Any]:
        """
        Call the provider API through backend gateway.
        
        Args:
            api_request: The API request
            
        Returns:
            API response with data, cost, and tokens
        """
        # TODO: Implement actual provider API calls through backend
        # For now, return mock response
        
        logger.info(
            f"📡 Calling {api_request.api_provider}/{api_request.model_name} "
            f"at {api_request.endpoint}"
        )
        
        # Mock response
        return {
            'data': {
                'message': 'Mock API response',
                'model': api_request.model_name
            },
            'cost': api_request.estimated_cost * 0.95,  # Simulate slight variance
            'tokens': api_request.estimated_tokens
        }


async def main():
    """Example usage of the agentic brain with decision engine."""
    brain = AgenticBrain()
    
    # Example request
    request = {
        'user_id': 'user_001',
        'project_id': 'proj_001',
        'agent_id': 'agent_flash_001',
        'api_provider': 'openai',
        'model_name': 'gpt-4',
        'endpoint': '/v1/chat/completions',
        'parameters': {
            'messages': [{'role': 'user', 'content': 'Hello!'}],
            'max_tokens': 100
        },
        'estimated_tokens': 100
    }
    
    result = await brain.process_request(request)
    print(f"\n{'='*60}")
    print(f"Result: {result['success']}")
    print(f"Message: {result['message']}")
    if result.get('decision'):
        print(f"Decision: {result['decision'].get('outcome')}")
        print(f"Agent Tier: {result['decision'].get('agent_tier')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
