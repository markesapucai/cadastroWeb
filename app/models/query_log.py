from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class QueryLog(Base):
    __tablename__ = "query_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    masked_document: Mapped[str] = mapped_column(String(20), nullable=False)  # Ex: ***.123.456-**
    doc_type: Mapped[str] = mapped_column(String(10), nullable=False)         # CPF ou CNPJ
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)        # Suporte para IPv6
    response_status: Mapped[int] = mapped_column(Integer, nullable=False)     # 200, 404, 500 etc.

    # Propriedade de relacionamento opcional (útil caso precisemos acessar email no log)
    # user = relationship("User")