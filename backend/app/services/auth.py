from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRecord(BaseModel):
    id: str
    tenant_id: str
    email: EmailStr
    password_hash: str


class AuthService:
    def __init__(self) -> None:
        self._users_by_email: dict[str, UserRecord] = {}

    def register(self, email: str, password: str, tenant_id: str = "demo-tenant") -> UserRecord:
        if email in self._users_by_email:
            raise ValueError("User already exists")
        user = UserRecord(id=email, tenant_id=tenant_id, email=email, password_hash=pwd_context.hash(password))
        self._users_by_email[email] = user
        return user

    def authenticate(self, email: str, password: str) -> UserRecord | None:
        user = self._users_by_email.get(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user

    def issue_access_token(self, user: UserRecord) -> str:
        settings = get_settings()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
        payload = {"sub": user.id, "tenant_id": user.tenant_id, "exp": expires_at}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


class AuthResult(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    tenant_id: str


auth_service = AuthService()
