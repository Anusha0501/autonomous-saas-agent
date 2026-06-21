from threading import RLock
from app.models.domain import AgentRun, ApprovalRequest


class InMemoryRunStore:
    """Development store. Replace with PostgreSQL repositories in production deployments."""

    def __init__(self) -> None:
        self._runs: dict[str, AgentRun] = {}
        self._lock = RLock()

    def create(self, run: AgentRun) -> AgentRun:
        with self._lock:
            self._runs[run.id] = run
            return run

    def list(self, tenant_id: str) -> list[AgentRun]:
        with self._lock:
            return [run for run in self._runs.values() if run.tenant_id == tenant_id]

    def get(self, run_id: str, tenant_id: str) -> AgentRun | None:
        with self._lock:
            run = self._runs.get(run_id)
            if not run or run.tenant_id != tenant_id:
                return None
            return run

    def save(self, run: AgentRun) -> AgentRun:
        with self._lock:
            run.touch()
            self._runs[run.id] = run
            return run

    def pending_approvals(self, tenant_id: str) -> list[ApprovalRequest]:
        approvals: list[ApprovalRequest] = []
        with self._lock:
            for run in self._runs.values():
                if run.tenant_id == tenant_id:
                    approvals.extend([approval for approval in run.approvals if approval.status == "pending"])
        return approvals


run_store = InMemoryRunStore()
