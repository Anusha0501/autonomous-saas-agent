# Autonomous SaaS Agent

A production-grade learning project for building an **Autonomous SaaS Agent** with FastAPI, React, LangGraph, LangChain, Pinecone, PostgreSQL, Redis, Docker, and LangSmith.

This repository is intentionally organized as a guided build. Following the teaching rules, implementation starts only after the foundational design artifacts are understood:

1. System Design
2. Architecture Diagram
3. Database Design
4. API Design

## Product Vision

The product accepts a user goal, plans work, researches context, executes approved actions, persists memory, requests human approval when risk is high, and delivers final results with traceability.

```text
User Goal
  ↓
Planner Agent
  ↓
Research Agent
  ↓
Execution Agent
  ↓
Memory Layer
  ↓
Human Approval
  ↓
Final Delivery
```

## Production Capabilities

- Authentication and tenant isolation
- LangGraph workflow orchestration
- Multi-agent planning, research, execution, and review
- Short-term and long-term memory
- PostgreSQL persistence
- Redis queues, locks, and rate limits
- Pinecone vector memory
- Human approval gates
- Checkpointing and resumability
- Structured logging and monitoring
- Error recovery and retries
- Cost tracking by tenant, user, run, model, and tool
- LangSmith tracing
- Docker-based local development
- Deployment path for Vercel frontend and Railway/Render backend

## Learning Outcomes

After completing this project, you should be able to:

- Build AI agents from scratch
- Build LangGraph workflows
- Build multi-agent systems
- Build memory systems
- Deploy production AI applications
- Prepare for AI Engineer and Agentic AI Engineer interviews

## Design Documents

- [System Design](docs/architecture/system-design.md)
- [Architecture Diagram](docs/architecture/architecture-diagram.md)
- [Database Design](docs/database/database-design.md)
- [API Design](docs/api/api-design.md)
- [Learning Path](docs/learning/learning-path.md)

## Teaching Contract

Each module follows this sequence:

1. Explain **why** the module exists.
2. Explain **what** will be built.
3. Explain **how** it works internally.
4. Implement the smallest production-worthy slice.
5. Add tests and observability.
6. Generate interview questions, quiz, and assignments.

## Quick Start

### Docker

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/health
- OpenAPI: http://localhost:8000/docs

### Backend Only

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

## Current Implementation Slice

This repository now includes a runnable vertical slice:

1. Submit a goal from the React dashboard.
2. FastAPI creates an agent run.
3. The workflow plans, researches, and stages high-risk execution for approval.
4. The user approves the run.
5. The workflow resumes, stores memory notes, tracks cost, and returns final delivery.

The first implementation uses an in-memory development store so the API and UI can be explored immediately. The database design documents define the PostgreSQL production model that will replace the development store in the persistence module.
