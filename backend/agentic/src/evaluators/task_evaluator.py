"""
Task Evaluation Logic
Handles evaluation of tasks and determines routing logic based on complexity and financial risk
"""
from google import genai
from dotenv import load_dotenv
import os


class TaskEvaluator:
    """Evaluates tasks and determines routing logic using our  AI"""
    
    def __init__(self, threshold=1.00):
        """
        Initialize task evaluator with AI-powered routing
        
        Args:
            threshold: Cost threshold for routing consideration (default $1.00)
        """
        self.threshold = threshold
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.router_prompt_template = """You are the SmartSpace  Controller. 
Analyze the User's Request for complexity and financial risk.

CRITERIA:
1. ROUTE TO 'FLASH' IF: 
   - Task is simple (chat, summary, translation, simple data extraction).
   - Estimated cost is likely under $1.00 USDC.

2. ROUTE TO 'PRO' IF:
   - Task is complex (requires visual analysis, heavy reasoning, or coding).
   - Task involves high-value purchases or sensitive financial decisions (> $1.00 USDC).
   - Task seems suspicious or malicious.

USER REQUEST: "{user_input}"
ESTIMATED COST: ${estimated_cost}

INSTRUCTION: Output ONLY one word: "FLASH" or "PRO". Do not explain."""

    def _get_ai_routing_decision(self, user_input, estimated_cost):
        """
        Use AI to determine optimal routing based on task complexity and risk
        
        Args:
            user_input: User's request text
            estimated_cost: Estimated cost in USDC
            
        Returns:
            str: "FLASH" or "PRO"
        """
        prompt = self.router_prompt_template.format(
            user_input=user_input,
            estimated_cost=estimated_cost
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            decision = response.text.strip().upper()
            # Ensure valid response
            if decision not in ["FLASH", "PRO"]:
                decision = "PRO" if estimated_cost > self.threshold else "FLASH"
            return decision
        except Exception as e:
            # Fallback to cost-based routing if AI fails
            print(f"Warning: AI routing failed, using fallback: {e}")
            return "PRO" if estimated_cost > self.threshold else "FLASH"
    
    def requires_auditor(self, estimated_cost):
        """
        Determine if task requires auditor review (PRO routing)
        
        Args:
            estimated_cost: Estimated cost in USDC
            
        Returns:
            bool: True if auditor (PRO) is required
        """
        return estimated_cost > self.threshold
    
    def evaluate_request(self, user_input, estimated_cost):
        """
        Evaluate a request and return routing decision using AI analysis
        
        Implements the SmartSpace Traffic Controller logic:
        - Analyzes task complexity
        - Considers financial risk
        - Detects suspicious requests
        - Routes to FLASH (fast) or PRO (careful) agent
        
        Args:
            user_input: User's request text
            estimated_cost: Estimated cost in USDC
            
        Returns:
            dict: Evaluation result with routing info
        """
        # Get AI-powered routing decision
        routing_decision = self._get_ai_routing_decision(user_input, estimated_cost)
        
        # Convert FLASH/PRO to agent type for backward compatibility
        agent_type = "auditor" if routing_decision == "PRO" else "cashier"
        
        return {
            "user_input": user_input,
            "estimated_cost": estimated_cost,
            "routing_decision": routing_decision,
            "agent_type": agent_type,
            "requires_auditor": routing_decision == "PRO"
        }
