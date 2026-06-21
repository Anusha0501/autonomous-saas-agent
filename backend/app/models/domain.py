from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4


class RunStatus(str, Enum):
    queued = "queued"
    running = "running"
    waiting_for_approval = "waiting_for_approval"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AgentTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    risk_level: RiskLevel = RiskLevel.low
    requires_approval: bool = False
    status: str = "planned"


class ApprovalRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    run_id: str
    task_id: str | None = None
    risk_level: RiskLevel
    proposed_action: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    decided_at: datetime | None = None
    decision_reason: str | None = None


class CostSummary(BaseModel):
    estimated_cost_usd: float = 0.0
    total_tokens: int = 0
    model_calls: int = 0
    tool_calls: int = 0


class AgentRun(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str
    user_id: str
    goal: str
    status: RunStatus = RunStatus.queued
    current_node: str = "queued"
    tasks: list[AgentTask] = Field(default_factory=list)
    research_notes: list[str] = Field(default_factory=list)
    tool_results: list[str] = Field(default_factory=list)
    approvals: list[ApprovalRequest] = Field(default_factory=list)
    final_output: str | None = None
    cost_summary: CostSummary = Field(default_factory=CostSummary)
    errors: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
