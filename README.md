# Agentic Commerce on Arc SmartSpace

An autonomous pay-per-use API access gateway with USDC payments, enabling secure API usage for AI agents and applications without exposing API keys.

## Project Overview

SmartSpace is a secure gateway that allows users and AI agents to call paid APIs (OpenAI, Google, Gemini, etc.) and pay instantly per request using USDC. Users do not need API keys, and billing remains controlled, transparent, and predictable.

For detailed project concept, see [idea.txt](./idea.txt)

## Repository Structure

This repository follows a monorepo structure with clear separation of concerns:

```
├── frontend/          # React-based frontend application
├── backend/           # Backend API and server logic
├── agentic/           # AI agent system code
├── idea.txt           # Project concept and requirements
└── README.md          # This file
```

### Frontend (`/frontend`)

React-based user interface for SmartSpace dashboard, authentication, and management.

**Tech Stack:**
- React 18
- React Router DOM
- Vite
- CSS

**Quick Start:**
```bash
cd frontend
npm install
npm run dev
```

See [frontend/README.md](./frontend/README.md) for detailed documentation.

### Backend (`/backend`)

Platform logic, API gateway, and server-side functionality.

**Responsibilities:**
- API request handling
- Payment processing integration
- User and project management
- Security and authentication
- Usage tracking and logging

**Status:** In development

See [backend/README.md](./backend/README.md) for setup instructions.

### Agentic System (`/agentic`)

AI agent logic, automation, and intelligent task processing.

**Responsibilities:**
- Agent orchestration
- Task evaluation and approval
- Autonomous API request handling
- Integration with backend gateway
- Result processing and feedback

**Status:** In development

See [agentic/README.md](./agentic/README.md) for documentation.

## Development Guidelines

### Folder Structure Standards

Each component (frontend, backend, agentic) should maintain its own:

- **README.md** - Component-specific documentation
- **package.json** / **requirements.txt** / etc. - Dependency management
- **.gitignore** - Component-specific ignore rules (if needed)
- **src/** or appropriate source directory
- **tests/** - Component-specific tests

### Committing Code

1. Work within your designated folder (`frontend/`, `backend/`, or `agentic/`)
2. Ensure your component's tests pass before committing
3. Update your component's README.md if adding new features
4. Use clear, descriptive commit messages

### Pull Requests

When submitting PRs:
- Clearly indicate which component(s) are affected
- Include setup/run instructions if dependencies change
- Update relevant README.md files
- Ensure code follows the existing patterns in your component

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/mudassirfayaz/Agentic-commerce-on-arc-smartSpace.git
cd Agentic-commerce-on-arc-smartSpace
```

2. Set up each component according to its README:
   - [Frontend Setup](./frontend/README.md)
   - [Backend Setup](./backend/README.md) (when available)
   - [Agentic Setup](./agentic/README.md) (when available)

## Core Features (MVP)

- [x] Frontend dashboard and authentication UI
- [ ] Create project or agent
- [ ] Set budgets and spending rules
- [ ] Per-request USDC payments
- [ ] Secure API execution
- [ ] Full usage + transaction logs
- [ ] No API key exposure

## Architecture Flow

```
User/Agent → SmartSpace evaluates + pays → SmartSpace calls API → Returns result + receipt
```

## Contributing

This is a hackathon project. Each developer should work within their designated component folder and maintain clean separation of concerns.

## License

[To be determined]

