from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Garante a injeção do driver assíncrono independentemente do formato do Render
uri = settings.DATABASE_URL
print("DATABASE_URL:", uri)
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql+asyncpg://", 1)
elif uri.startswith("postgresql://") and not uri.startswith("postgresql+asyncpg://"):
    uri = uri.replace("postgresql://", "postgresql+asyncpg://", 1)

SQLALCHEMY_DATABASE_URL = uri
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass