# Agentic System

AI agent logic, automation, and intelligent task processing for SmartSpace.

## Responsibilities

- Agent orchestration and coordination
- Task evaluation and approval workflows
- Autonomous API request handling
- Integration with SmartSpace backend gateway
- Result processing and feedback loops
- Intelligent routing and decision making

## Status

✅ **Core System Complete** - Basic architecture and agent workflow implemented.

## Tech Stack

- **Language**: Python 3.10+
- **AI Framework**: Google Gemini API (google-genai)
- **Package Manager**: uv
- **Environment**: python-dotenv

## Folder Structure

agentic/
├── src/
│   ├── agents/              # AI agent orchestration
│   │   └── gemini_agent.py  # Cashier & Auditor agents
│   ├── tasks/               # Task management
│   │   └── processor.py     # Main workflow orchestrator
│   ├── evaluators/          # Task evaluation logic
│   │   └── task_evaluator.py
│   ├── integrations/        # External system interfaces
│   │   └── payment_handler.py
│   └── utils/               # Utilities and helpers
│       └── tools.py
├── tests/                   # Unit & integration tests
│   ├── test_evaluator.py
│   └── test_payment_handler.py
├── config/                  # Configuration files
│   ├── config.py
│   └── settings.env.example
├── main.py       # Demo entry point
└── README.md                # This file

## Architecture

The agentic system integrates with:
- **Backend API** - For request processing and payment handling (pending integration)
- **External APIs** - Via SmartSpace gateway (never directly) (pending integration)
- **Payment System** - Through backend integration (pending Arc/Circle)

### Current Implementation

✅ **Dual-Agent System**
- **FlashModel**: Fast processing for micro-transactions (< $1.00)
- **ProModel**: Careful analysis for high-value requests (> $1.00)

✅ **Intelligent Routing**
- Automatic cost-based routing
- Configurable thresholds
- Agent selection optimization

✅ **Function Calling**
- AI agents can approve/reject payments
- Structured tool declarations
- Automated execution flow

## Agent Workflow

The system implements this 5-step workflow:

1. **Receive task request** - Via TaskProcessor
2. **Evaluate task requirements and costs** - Via TaskEvaluator  
3. **Request approval/payment via backend** - Via Payment Handlers (mock for now)
4. **Execute API calls through SmartSpace gateway** - (Pending backend integration)
5. **Process results and provide feedback** - Via AI Agents

## Features


### Pending 🚧

- Backend API integration
- SmartSpace gateway connection
- Arc/Circle payment system
- Database persistence
- Real-time monitoring

## Contributing

When adding features:
1. Follow existing module structure
2. Add tests for new functionality
3. Update documentation
4. Ensure all tests pass

