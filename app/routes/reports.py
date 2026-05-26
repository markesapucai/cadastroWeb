from fastapi import APIRouter, Depends
from app.services.report_service import ReportService
from app.core.dependencies import get_report_service, get_current_user_id

router = APIRouter(prefix="/reports", tags=["Relatórios"])

@router.get("/billing")
async def get_billing_report(
    year: int,
    month: int,
    user_id: int = Depends(get_current_user_id),
    report_service: ReportService = Depends(get_report_service)
):
    return await report_service.get_monthly_billing_report(year, month)