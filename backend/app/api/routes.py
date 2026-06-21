from fastapi import APIRouter, Depends, Header, HTTPException
from app.agents.workflow import workflow
from app.core.config import Settings, get_settings
from app.models.domain import AgentRun
from app.schemas.api import AuthRequest, AuthResponse, CreateRunRequest, DecisionRequest, HealthResponse, RunListResponse
from app.services.auth import auth_service
from app.services.store import run_store

router = APIRouter()


def get_context(x_tenant_id: str = Header(default="demo-tenant"), x_user_id: str = Header(default="demo-user")) -> tuple[str, str]:
    return x_tenant_id, x_user_id


@router.post("/auth/register", response_model=AuthResponse, status_code=201)
def register(payload: AuthRequest) -> AuthResponse:
    try:
        user = auth_service.register(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    token = auth_service.issue_access_token(user)
    return AuthResponse(access_token=token, token_type="bearer", user_id=user.id, tenant_id=user.tenant_id)


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: AuthRequest) -> AuthResponse:
    user = auth_service.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth_service.issue_access_token(user)
    return AuthResponse(access_token=token, token_type="bearer", user_id=user.id, tenant_id=user.tenant_id)


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name, environment=settings.environment)


@router.get("/ready", response_model=HealthResponse)
def ready(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(status="ready", service=settings.app_name, environment=settings.environment)


@router.post("/runs", response_model=AgentRun, status_code=201)
def create_run(payload: CreateRunRequest, context: tuple[str, str] = Depends(get_context)) -> AgentRun:
    tenant_id, user_id = context
    run = AgentRun(tenant_id=tenant_id, user_id=user_id, goal=payload.goal)
    run_store.create(run)
    workflow.start(run, payload.constraints.budget_usd, payload.constraints.requires_approval_for_external_actions)
    return run_store.save(run)


@router.get("/runs", response_model=RunListResponse)
def list_runs(context: tuple[str, str] = Depends(get_context)) -> RunListResponse:
    tenant_id, _ = context
    return RunListResponse(runs=run_store.list(tenant_id))


@router.get("/runs/{run_id}", response_model=AgentRun)
def get_run(run_id: str, context: tuple[str, str] = Depends(get_context)) -> AgentRun:
    tenant_id, _ = context
    run = run_store.get(run_id, tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/approvals/{run_id}/approve", response_model=AgentRun)
def approve(run_id: str, payload: DecisionRequest, context: tuple[str, str] = Depends(get_context)) -> AgentRun:
    tenant_id, _ = context
    run = run_store.get(run_id, tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    workflow.resume_after_approval(run, approved=True, reason=payload.reason)
    return run_store.save(run)


@router.post("/approvals/{run_id}/reject", response_model=AgentRun)
def reject(run_id: str, payload: DecisionRequest, context: tuple[str, str] = Depends(get_context)) -> AgentRun:
    tenant_id, _ = context
    run = run_store.get(run_id, tenant_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    workflow.resume_after_approval(run, approved=False, reason=payload.reason)
    return run_store.save(run)


@router.get("/approvals")
def approvals(context: tuple[str, str] = Depends(get_context)) -> dict:
    tenant_id, _ = context
    return {"approvals": run_store.pending_approvals(tenant_id)}
