# Architecture Diagram

## High-Level Architecture

```mermaid
flowchart TD
    U[User] --> FE[React Frontend on Vercel]
    FE --> API[FastAPI Backend on Railway or Render]
    API --> AUTH[Auth Service]
    API --> RUNS[Agent Run Service]
    RUNS --> QUEUE[Redis Queue and Locks]
    QUEUE --> WORKER[Agent Worker]
    WORKER --> GRAPH[LangGraph Workflow]
    GRAPH --> PLANNER[Planner Agent]
    GRAPH --> RESEARCH[Research Agent]
    GRAPH --> EXEC[Execution Agent]
    GRAPH --> REVIEW[Reviewer Agent]
    GRAPH --> APPROVAL[Human Approval Node]
    GRAPH --> MEMORY[Memory Manager]
    MEMORY --> PG[(PostgreSQL)]
    MEMORY --> PINE[(Pinecone Vector Index)]
    RUNS --> PG
    API --> PG
    API --> REDIS[(Redis)]
    WORKER --> LANGSMITH[LangSmith Tracing]
    API --> LOGS[Structured Logs and Metrics]
    WORKER --> TOOLS[External Tools]
    APPROVAL --> PG
    FE --> STREAM[Run Status Stream]
    API --> STREAM
```

## LangGraph Workflow

```mermaid
stateDiagram-v2
    [*] --> LoadContext
    LoadContext --> Plan
    Plan --> Research
    Research --> Execute
    Execute --> NeedsApproval
    NeedsApproval --> ApprovalPaused: risky action
    ApprovalPaused --> Execute: approved
    ApprovalPaused --> RevisePlan: rejected or changes requested
    NeedsApproval --> Review: safe action
    RevisePlan --> Plan
    Review --> Research: insufficient evidence
    Review --> Execute: incomplete execution
    Review --> SaveMemory: accepted
    SaveMemory --> FinalDelivery
    FinalDelivery --> [*]
```

## Why This Architecture

- **FastAPI** provides a typed, async backend boundary for auth, APIs, webhooks, and streaming run updates.
- **React** gives users a clear workspace for goals, plans, research, approvals, and final delivery.
- **LangGraph** makes the agent workflow explicit, resumable, testable, and safe to interrupt.
- **PostgreSQL** stores authoritative SaaS data, run state, checkpoints, approvals, and cost records.
- **Redis** supports fast coordination: queues, locks, idempotency, rate limits, and ephemeral status.
- **Pinecone** provides semantic retrieval for long-term memories and research artifacts.
- **LangSmith** gives model/tool traces required for debugging and evaluation.

## Deployment Topology

```mermaid
flowchart LR
    GH[GitHub] --> V[Vercel Frontend]
    GH --> R[Railway or Render Backend]
    R --> PSQL[(Managed PostgreSQL)]
    R --> RD[(Managed Redis)]
    R --> PC[(Pinecone)]
    R --> LS[LangSmith]
```
