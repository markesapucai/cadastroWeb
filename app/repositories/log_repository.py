from datetime import datetime
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.query_log import QueryLog

class LogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_log(self, user_id: int, masked_document: str, doc_type: str, ip_address: str, response_status: int) -> QueryLog:
        """
        Cria um registro de auditoria de consulta.
        Note que NÃO recebemos os dados da pessoa, apenas o documento mascarado e os metadados.
        """
        log = QueryLog(
            user_id=user_id,
            masked_document=masked_document,
            doc_type=doc_type,
            ip_address=ip_address,
            response_status=response_status
        )
        self.session.add(log)
        await self.session.commit()
        await self.session.refresh(log)
        
        return log

    async def get_logs_by_period(self, start_date: datetime, end_date: datetime) -> Sequence[QueryLog]:
        """
        Busca os logs de um período específico para compor o relatório de utilização mensal.
        """
        stmt = select(QueryLog).where(
            QueryLog.timestamp >= start_date,
            QueryLog.timestamp <= end_date
        ).order_by(QueryLog.timestamp.desc())
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
        
    async def get_recent_logs(self, limit: int = 5) -> Sequence[QueryLog]:
        """
        Busca as últimas consultas realizadas para exibir no Dashboard inicial.
        """
        stmt = select(QueryLog).order_by(QueryLog.timestamp.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()