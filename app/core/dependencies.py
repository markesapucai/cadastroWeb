import httpx
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import SessionLocal
from app.core.config import settings
from app.core.security import JWTHandler
from app.repositories.user_repository import UserRepository
from app.repositories.log_repository import LogRepository
from app.services.auth_service import AuthService
from app.services.query_service import QueryService
from app.services.report_service import ReportService
from app.services.cpfcnpj_client import CPFCNPJClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# --- Instâncias Base ---
def get_jwt_handler() -> JWTHandler:
    return JWTHandler(secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

async def get_http_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client

# --- Repositórios ---
def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session=db)

def get_log_repository(db: AsyncSession = Depends(get_db)) -> LogRepository:
    return LogRepository(session=db)

# --- Serviços ---
def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
) -> AuthService:
    return AuthService(user_repo=user_repo, jwt_handler=jwt_handler)

def get_query_service(
    http_client: httpx.AsyncClient = Depends(get_http_client),
    log_repo: LogRepository = Depends(get_log_repository)
) -> QueryService:
    client = CPFCNPJClient(http_client=http_client)
    return QueryService(client=client, log_repo=log_repo)

def get_report_service(log_repo: LogRepository = Depends(get_log_repository)) -> ReportService:
    return ReportService(log_repo=log_repo)

# --- Autenticação do Usuário Logado ---
async def get_current_user_id(
    token: str = Depends(oauth2_scheme), 
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
) -> int:
    try:
        payload = jwt_handler.decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return int(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado ou inválido")