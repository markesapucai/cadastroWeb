from fastapi import APIRouter, Depends
from app.services.report_service import ReportService
from app.core.dependencies import get_report_service, get_current_user_id

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_summary(
    user_id: int = Depends(get_current_user_id),
    report_service: ReportService = Depends(get_report_service)
):
    # O user_id é injetado apenas para garantir que a rota é protegida (autenticada)
    return await report_service.get_dashboard_summary()