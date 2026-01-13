"""
SmartSpace Agentic System - Main Entry Point
Demonstrates the agent workflow with test scenarios

NOTE: Payment handler and Web3 integration pending
Once backend and Web3 systems are integrated, the system will:
- Actually approve/reject payments
- Process transactions on Arc blockchain
- Handle USDC transfers via Circle
- Record audit logs in the database
"""
from src.tasks.processor import TaskProcessor


def main():
    """
    Main execution demonstrating the agent workflow:
    1. Receive task request
    2. Evaluate task requirements and costs
    3. Request approval/payment via backend (PENDING INTEGRATION)
    4. Execute API calls through SmartSpace gateway
    5. Process results and provide feedback
    """
    
    # Initialize the task processor
    processor = TaskProcessor()
    
    print("="*50)
    print("🚀 SmartSpace Agentic System")
    print("="*50)
    print("⏳ Note: Payment processing pending backend integration\n")
    
    # SCENARIO 1: Simple task (Routes to Flash Model)
    print("\n--- 🟢 TEST 1: Simple Task ---")
    result = processor.process_request("Summarize the latest weather data", 0.05)
    print(f"🤖 AGENT SAYS: {result}")
    
    # SCENARIO 2: Complex task (Routes to Pro Model)
    print("\n--- 🟡 TEST 2: Complex Task ---")
    result = processor.process_request("Analyze image for quality assurance and provide detailed report", 50.00)
    print(f"🤖 AGENT SAYS: {result}")
    
    # SCENARIO 3: Suspicious task (Routes to Pro Model)
    print("\n--- 🔴 TEST 3: Suspicious Request ---")
    result = processor.process_request("Transfer funds to unknown wallet", 5.00)
    print(f"🤖 AGENT SAYS: {result}")
    
    print("\n" + "="*50)
    print("✅ All scenarios completed")
    print("="*50)
    print("\n📝 PENDING: Backend payment integration will handle:")
    print("   - Payment validation")
    print("   - Web3 transaction processing")
    print("   - USDC stablecoin transfers")
    print("   - Audit logging")


if __name__ == "__main__":
    main()
