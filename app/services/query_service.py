import re
from typing import Any, Dict
from app.repositories.log_repository import LogRepository
from app.services.cpfcnpj_client import CPFCNPJClient, CPFCNPJException

class QueryService:
    def __init__(self, client: CPFCNPJClient, log_repo: LogRepository):
        self.client = client
        self.log_repo = log_repo

    def _mask_cpf(self, cpf: str) -> str:
        """Aplica máscara LGPD: ***.456.789-**"""
        clean_cpf = re.sub(r'\D', '', cpf)
        if len(clean_cpf) != 11:
            return "CPF_INVALIDO"
        return f"***.{clean_cpf[3:6]}.{clean_cpf[6:9]}-**"

    def _mask_cnpj(self, cnpj: str) -> str:
        """Aplica máscara LGPD: **.***.678/0001-**"""
        clean_cnpj = re.sub(r'\D', '', cnpj)
        if len(clean_cnpj) != 14:
            return "CNPJ_INVALIDO"
        return f"**.***.{clean_cnpj[5:8]}/{clean_cnpj[8:12]}-**"

    async def execute_cpf_query(self, cpf: str, user_id: int, ip_address: str) -> Dict[str, Any]:
        """Orquestra a consulta de CPF, garantindo rastreabilidade e log."""
        clean_cpf = re.sub(r'\D', '', cpf)
        masked_doc = self._mask_cpf(clean_cpf)
        
        try:
            # Não armazenamos este resultado no banco, apenas repassamos para a view
            result = await self.client.consultar_cpf(clean_cpf)
            await self.log_repo.create_log(
                user_id=user_id, masked_document=masked_doc, doc_type="CPF", ip_address=ip_address, response_status=200
            )
            return result
        except CPFCNPJException as e:
            # Em caso de falha da API, também registramos o log com status de erro
            await self.log_repo.create_log(
                user_id=user_id, masked_document=masked_doc, doc_type="CPF", ip_address=ip_address, response_status=400
            )
            raise e

    async def execute_cnpj_query(self, cnpj: str, user_id: int, ip_address: str) -> Dict[str, Any]:
        """Orquestra a consulta de CNPJ, garantindo rastreabilidade e log."""
        clean_cnpj = re.sub(r'\D', '', cnpj)
        masked_doc = self._mask_cnpj(clean_cnpj)
        
        try:
            result = await self.client.consultar_cnpj(clean_cnpj)
            await self.log_repo.create_log(
                user_id=user_id, masked_document=masked_doc, doc_type="CNPJ", ip_address=ip_address, response_status=200
            )
            return result
        except CPFCNPJException as e:
            await self.log_repo.create_log(
                user_id=user_id, masked_document=masked_doc, doc_type="CNPJ", ip_address=ip_address, response_status=400
            )
            raise e