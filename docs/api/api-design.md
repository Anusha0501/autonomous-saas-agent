# API Design

## Why The API Boundary Matters

The API is the safety boundary between users, agents, tools, and persisted state. It must validate identity, enforce tenant authorization, expose workflow status, and make human approvals explicit.

## API Principles

- REST for core resources
- Server-sent events or WebSockets for run updates
- Idempotency keys for goal submission and approval decisions
- Tenant isolation on every request
- Explicit status transitions
- No direct client access to model provider or tool secrets

## Authentication

| Method | Purpose |
| --- | --- |
| Email/password or OAuth | User login |
| JWT access token | Short-lived API authorization |
| Refresh token | Session continuation with rotation |
| Hashed API keys | Server-to-server integrations |

## Core Endpoints

### Auth

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Create tenant owner and user |
| `POST` | `/api/auth/login` | Authenticate user |
| `POST` | `/api/auth/refresh` | Rotate access token |
| `POST` | `/api/auth/logout` | Revoke refresh token |

### Agent Runs

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/runs` | Submit a user goal |
| `GET` | `/api/runs` | List runs for the tenant |
| `GET` | `/api/runs/{run_id}` | Get run detail |
| `GET` | `/api/runs/{run_id}/events` | Stream run status updates |
| `POST` | `/api/runs/{run_id}/cancel` | Cancel a queued or running workflow |
| `POST` | `/api/runs/{run_id}/retry` | Retry from latest safe checkpoint |

### Approvals

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/approvals` | List pending approvals |
| `GET` | `/api/approvals/{approval_id}` | Inspect proposed action |
| `POST` | `/api/approvals/{approval_id}/approve` | Approve and resume graph |
| `POST` | `/api/approvals/{approval_id}/reject` | Reject and route graph to revision |
| `POST` | `/api/approvals/{approval_id}/request-changes` | Ask agent to revise plan/action |

### Memory

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/memories` | List user or tenant memories |
| `POST` | `/api/memories` | Create an explicit memory |
| `PATCH` | `/api/memories/{memory_id}` | Update memory text or metadata |
| `DELETE` | `/api/memories/{memory_id}` | Remove memory and vector reference |

### Cost and Monitoring

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/costs/summary` | Cost by tenant, user, model, and run |
| `GET` | `/api/health` | Liveness check |
| `GET` | `/api/ready` | Dependency readiness check |

## Request and Response Examples

### Submit Goal

```json
{
  "goal": "Research competitors and draft a launch plan for my AI note-taking SaaS.",
  "constraints": {
    "budget_usd": 5,
    "requires_approval_for_external_actions": true
  }
}
```

### Run Status Response

```json
{
  "id": "run_123",
  "status": "waiting_for_approval",
  "current_node": "human_approval",
  "goal": "Research competitors and draft a launch plan for my AI note-taking SaaS.",
  "cost_summary": {
    "estimated_cost_usd": 1.42,
    "total_tokens": 18420
  }
}
```

## Error Contract

All errors should follow a stable shape:

```json
{
  "error": {
    "code": "approval_required",
    "message": "This action requires human approval before execution.",
    "request_id": "req_abc123",
    "details": {}
  }
}
```

## API Learning Checks

### Interview Questions

1. Why should approval decisions use idempotency keys?
2. Why should frontend clients never call model providers directly in this architecture?
3. What is the difference between `/health` and `/ready`?
4. How would you stream long-running LangGraph progress to the frontend?

### Quiz

1. Which endpoint resumes a graph after approval?
2. Which endpoint should expose dependency readiness?
3. Why should every error include a request ID?

### Assignments

1. Design the TypeScript type for `AgentRun`.
2. Design the Python Pydantic schema for `CreateRunRequest`.
3. Write five API authorization test cases.
