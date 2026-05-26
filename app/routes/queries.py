from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas.query import DocumentQuery
from app.services.query_service import QueryService
from app.services.cpfcnpj_client import CPFCNPJException
from app.core.dependencies import get_query_service, get_current_user_id

router = APIRouter(prefix="/queries", tags=["Consultas"])

def get_client_ip(request: Request) -> str:
    return request.client.host if request.client else "0.0.0.0"

@router.post("/cpf")
async def consultar_cpf(
    request: Request,
    query: DocumentQuery,
    user_id: int = Depends(get_current_user_id),
    query_service: QueryService = Depends(get_query_service)
):
    try:
        ip_address = get_client_ip(request)
        result = await query_service.execute_cpf_query(query.document, user_id, ip_address)
        return result
    except CPFCNPJException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/cnpj")
async def consultar_cnpj(
    request: Request,
    query: DocumentQuery,
    user_id: int = Depends(get_current_user_id),
    query_service: QueryService = Depends(get_query_service)
):
    try:
        ip_address = get_client_ip(request)
        result = await query_service.execute_cnpj_query(query.document, user_id, ip_address)
        return result
    except CPFCNPJException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))