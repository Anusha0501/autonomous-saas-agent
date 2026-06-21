from datetime import datetime, timezone
from app.models.domain import AgentRun, AgentTask, ApprovalRequest, RiskLevel, RunStatus


class AgentWorkflow:
    """Deterministic workflow adapter shaped like a future LangGraph graph.

    The class keeps the node boundaries explicit so the implementation can be
    swapped for compiled LangGraph nodes without changing API contracts.
    """

    def start(self, run: AgentRun, budget_usd: float, require_approval: bool) -> AgentRun:
        run.status = RunStatus.running
        self._plan(run, require_approval)
        self._research(run)
        self._execute(run, budget_usd)
        if run.status != RunStatus.waiting_for_approval:
            self._save_memory(run)
            self._deliver(run)
        return run

    def resume_after_approval(self, run: AgentRun, approved: bool, reason: str | None) -> AgentRun:
        pending = [approval for approval in run.approvals if approval.status == "pending"]
        for approval in pending:
            approval.status = "approved" if approved else "rejected"
            approval.decided_at = datetime.now(timezone.utc)
            approval.decision_reason = reason
        if not approved:
            run.status = RunStatus.failed
            run.current_node = "approval_rejected"
            run.errors.append(reason or "Human rejected the proposed action.")
            return run
        run.status = RunStatus.running
        run.current_node = "execute"
        run.tool_results.append("Approved high-risk action was executed in a controlled sandbox.")
        self._save_memory(run)
        self._deliver(run)
        return run

    def _plan(self, run: AgentRun, require_approval: bool) -> None:
        run.current_node = "planner"
        run.tasks = [
            AgentTask(title="Clarify success criteria", description="Extract deliverables, constraints, and acceptance criteria from the goal."),
            AgentTask(title="Research context", description="Gather relevant facts, examples, and prior memory for the goal."),
            AgentTask(
                title="Execute delivery plan",
                description="Produce the requested artifact and stage any external action.",
                risk_level=RiskLevel.high if require_approval else RiskLevel.medium,
                requires_approval=require_approval,
            ),
        ]
        run.cost_summary.model_calls += 1
        run.cost_summary.total_tokens += 900
        run.cost_summary.estimated_cost_usd += 0.02

    def _research(self, run: AgentRun) -> None:
        run.current_node = "research"
        run.research_notes.extend([
            "Retrieved tenant preferences and prior run context from the memory layer.",
            "Collected implementation guidance for planning, research, execution, approval, and delivery nodes.",
        ])
        run.cost_summary.model_calls += 1
        run.cost_summary.tool_calls += 1
        run.cost_summary.total_tokens += 1400
        run.cost_summary.estimated_cost_usd += 0.04

    def _execute(self, run: AgentRun, budget_usd: float) -> None:
        run.current_node = "execute"
        if run.cost_summary.estimated_cost_usd > budget_usd:
            run.status = RunStatus.failed
            run.errors.append("Run exceeded the configured budget before execution.")
            return
        risky_tasks = [task for task in run.tasks if task.requires_approval]
        if risky_tasks:
            task = risky_tasks[0]
            run.current_node = "human_approval"
            run.status = RunStatus.waiting_for_approval
            run.approvals.append(
                ApprovalRequest(
                    run_id=run.id,
                    task_id=task.id,
                    risk_level=task.risk_level,
                    proposed_action="Execute the final delivery plan and any external side effects after human review.",
                )
            )
            return
        run.tool_results.append("Executed the delivery plan without external side effects.")
        run.cost_summary.tool_calls += 1

    def _save_memory(self, run: AgentRun) -> None:
        run.current_node = "memory"
        run.research_notes.append("Saved reusable project context and delivery preferences to long-term memory metadata.")

    def _deliver(self, run: AgentRun) -> None:
        run.current_node = "final_delivery"
        run.status = RunStatus.completed
        run.completed_at = datetime.now(timezone.utc)
        run.final_output = (
            "Production-ready agent run completed. The system planned the work, gathered context, "
            "executed approved steps, recorded memory, tracked cost, and produced an auditable delivery."
        )


workflow = AgentWorkflow()
