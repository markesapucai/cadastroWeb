from datetime import datetime, timezone
import calendar
from typing import Dict, Any, List
from app.repositories.log_repository import LogRepository

class ReportService:
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo
        self.CUSTO_POR_CONSULTA = 0.25 # RNF05: Custo estimado

    async def get_dashboard_summary(self) -> Dict[str, Any]:
        """Gera os totalizadores para a tela inicial (RF06)."""
        now = datetime.now(timezone.utc)
        
        # Início do mês atual
        start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        
        # Busca dados nos repositórios
        recent_logs = await self.log_repo.get_recent_logs(limit=5)
        monthly_logs = await self.log_repo.get_logs_by_period(start_of_month, now)
        
        # Processamento em memória
        total_month = len(monthly_logs)
        total_today = sum(1 for log in monthly_logs if log.timestamp.date() == now.date())
        
        return {
            "total_month": total_month,
            "total_today": total_today,
            "recent_queries": [
                {
                    "doc": log.masked_document, 
                    "type": log.doc_type, 
                    "time": log.timestamp.strftime("%d/%m/%Y %H:%M")
                } 
                for log in recent_logs
            ]
        }
        
    async def get_monthly_billing_report(self, year: int, month: int) -> Dict[str, Any]:
        """Gera o relatório de faturamento do mês específico (RF05)."""
        # Calcular último dia do mês
        last_day = calendar.monthrange(year, month)[1]
        start_date = datetime(year, month, 1, tzinfo=timezone.utc)
        end_date = datetime(year, month, last_day, 23, 59, 59, tzinfo=timezone.utc)
        
        logs = await self.log_repo.get_logs_by_period(start_date, end_date)
        
        # Filtra apenas requisições com sucesso (status 200) para tarifação
        successful_queries = [log for log in logs if log.response_status == 200]
        total_queries = len(successful_queries)
        
        return {
            "period": f"{month:02d}/{year}",
            "total_queries": total_queries,
            "estimated_cost": total_queries * self.CUSTO_POR_CONSULTA,
            "logs": logs
        }