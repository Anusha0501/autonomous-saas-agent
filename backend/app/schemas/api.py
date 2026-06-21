from pydantic import BaseModel, Field
from app.models.domain import AgentRun


class GoalConstraints(BaseModel):
    budget_usd: float = Field(default=5.0, ge=0)
    requires_approval_for_external_actions: bool = True


class CreateRunRequest(BaseModel):
    goal: str = Field(min_length=10, max_length=4000)
    constraints: GoalConstraints = Field(default_factory=GoalConstraints)


class DecisionRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=1000)


class RunListResponse(BaseModel):
    runs: list[AgentRun]


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str


class AuthRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=256)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    tenant_id: str
