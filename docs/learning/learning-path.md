# Learning Path

## Teaching Method

For every module, learn in this order:

1. **Why**: the production problem the module solves.
2. **What**: the component, interface, and acceptance criteria.
3. **How**: the internal design, data flow, and trade-offs.
4. **Implementation**: the smallest production-grade slice.
5. **Evaluation**: tests, traces, metrics, and failure cases.
6. **Career Prep**: interview questions, quiz, and assignments.

## Module Roadmap

| Module | Outcome | Core Concepts |
| --- | --- | --- |
| 0. Design Foundation | Understand system, architecture, DB, and API design | SaaS boundaries, workflow design |
| 1. Local Platform | Run backend, frontend, DB, Redis in Docker | Docker, settings, health checks |
| 2. Authentication | Secure tenant-aware login | JWT, refresh rotation, RBAC |
| 3. Agent Run Model | Persist and list user goals | PostgreSQL, migrations, service layer |
| 4. LangGraph Basics | Execute a minimal graph | state, nodes, edges, checkpoints |
| 5. Tool Calling | Add safe tools with schemas | validation, idempotency, audit logs |
| 6. Research Agent | Gather sourced context | retrieval, citations, confidence |
| 7. Planner Agent | Decompose goals into tasks | task planning, risk classification |
| 8. Execution Agent | Execute approved actions | tool policies, retries, recovery |
| 9. Memory Layer | Store and retrieve user context | Pinecone, embeddings, memory types |
| 10. Human Approval | Pause and resume workflows | approvals, checkpoints, UX |
| 11. Multi-Agent Review | Add reviewer and revision loops | critique, evals, graph cycles |
| 12. Observability | Trace, log, and monitor runs | LangSmith, metrics, structured logs |
| 13. Cost Tracking | Enforce budgets and quotas | token accounting, cost dashboards |
| 14. Deployment | Ship frontend and backend | Vercel, Railway/Render, secrets |
| 15. Interview Capstone | Explain and defend the architecture | system design, debugging, trade-offs |

## Global Assignments

1. Keep an architecture decision record for every major trade-off.
2. After each module, write one failure postmortem for a realistic incident.
3. Build a demo script that explains the system in five minutes.
4. Prepare STAR-format interview stories for debugging, design, and deployment decisions.
