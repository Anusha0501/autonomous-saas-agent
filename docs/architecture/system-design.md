# System Design

## 1. Why This System Exists

Most AI demos stop at a single chatbot. A production autonomous SaaS agent needs more than prompting: it requires orchestration, persistence, memory, approvals, observability, security, and recovery. This system is designed to teach and implement those production concerns incrementally.

## 2. What We Are Building

A multi-tenant SaaS application where authenticated users create goals. Each goal becomes an agent run managed by a LangGraph workflow:

1. **Planner Agent** decomposes the goal into tasks.
2. **Research Agent** gathers facts and context using tools and memory.
3. **Execution Agent** performs safe actions or prepares proposed actions.
4. **Memory Layer** stores user preferences, run artifacts, decisions, and embeddings.
5. **Human Approval** pauses risky or irreversible actions.
6. **Final Delivery** returns a traceable result with sources, costs, and run history.

## 3. How The System Works

### Core Runtime Flow

1. User submits a goal through the React app.
2. FastAPI validates authentication and creates an `agent_runs` record.
3. A background worker starts or resumes a LangGraph workflow.
4. LangGraph routes state between planner, researcher, executor, approval, and delivery nodes.
5. PostgreSQL stores durable state, checkpoints, approvals, audit logs, and cost records.
6. Redis handles queues, locks, idempotency keys, rate limits, and temporary run state.
7. Pinecone stores semantic memory and retrieved knowledge chunks.
8. LangSmith receives traces for prompts, tools, model calls, latency, and errors.
9. The frontend streams status updates and renders approval requests.

### Agent Responsibilities

| Agent | Responsibility | Inputs | Outputs |
| --- | --- | --- | --- |
| Planner Agent | Break goals into typed tasks and risk levels | User goal, user memory, tenant policy | Plan, task graph, approval requirements |
| Research Agent | Collect and synthesize context | Plan tasks, tools, memory | Research notes, sources, confidence |
| Execution Agent | Execute allowed tasks and stage risky tasks | Research, plan, tool registry | Tool results, proposed actions, errors |
| Reviewer Agent | Evaluate quality, safety, and completeness | Run state, outputs, policies | Pass/fail, revision requests |
| Memory Manager | Save and retrieve durable context | User profile, run events, artifacts | Memories, embeddings, retrieval results |

### State Model

The LangGraph state should include:

- `run_id`
- `tenant_id`
- `user_id`
- `goal`
- `plan`
- `tasks`
- `research_notes`
- `tool_results`
- `approval_requests`
- `memory_context`
- `cost_summary`
- `errors`
- `final_answer`

### Human Approval Strategy

Human approval is required when a task is:

- Irreversible
- External-facing
- Costly beyond tenant limits
- Permission-sensitive
- Low-confidence
- Security-sensitive

The graph pauses at an approval node, persists a checkpoint, and resumes after the user approves, rejects, or requests changes.

### Error Recovery Strategy

Production agents fail in predictable ways. The design includes:

- Retry policies for transient tool and model failures
- Circuit breakers for failing integrations
- Idempotency keys for repeated execution requests
- Checkpoint resume for interrupted runs
- Dead-letter queues for jobs that exceed retry limits
- User-visible failure summaries with next actions

### Cost Tracking Strategy

Every model and tool call records:

- Tenant and user
- Run and node
- Provider and model
- Prompt, completion, and total tokens
- Estimated and actual cost
- Latency
- Success or failure

### Security Boundaries

- JWT authentication with refresh token rotation
- Tenant-scoped authorization checks on every resource
- Row-level ownership checks at service boundaries
- Tool allowlists by tenant and environment
- Secrets stored only in deployment providers, never in source code
- Audit logs for approvals and external actions

## 4. Initial Module Sequence

1. Repository and Docker foundation
2. FastAPI health, auth, and tenant model
3. PostgreSQL schema and migrations
4. LangGraph minimal workflow
5. Agent run API and streaming status
6. Memory layer with Pinecone and PostgreSQL
7. Human approval checkpointing
8. Observability, logging, and LangSmith
9. Cost tracking and quotas
10. Deployment hardening

## Module 0 Learning Checks

### Interview Questions

1. Why is LangGraph preferred over a simple chain for long-running agent workflows?
2. What is the difference between checkpointing and memory?
3. How do human approval gates reduce production risk?
4. Why should cost tracking be modeled as first-class data?
5. How would you prevent an execution agent from repeating an external action after a retry?

### Quiz

1. Which datastore should own durable relational run state: PostgreSQL, Redis, or Pinecone?
2. Which system should store semantic long-term memory?
3. What should happen before an irreversible external action?
4. Why should every tool call include tenant and run identifiers?

### Assignments

1. Write three example user goals and classify their risk levels.
2. Design a failure scenario for each agent and explain the recovery path.
3. Define five tenant-level limits that a SaaS admin should configure.
