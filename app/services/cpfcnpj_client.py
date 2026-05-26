import httpx
from typing import Any, Dict
from app.core.config import settings

# --- Exceções Customizadas do Domínio ---

class CPFCNPJException(Exception):
    """Exceção base para a API CPF/CNPJ."""
    pass

class InsufficientCreditsException(CPFCNPJException):
    pass

class InvalidDocumentException(CPFCNPJException):
    pass

class APIUnavailableException(CPFCNPJException):
    pass

class APITimeoutException(CPFCNPJException):
    pass


# --- Cliente da API ---

class CPFCNPJClient:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client
        self.base_url = "https://api.cpfcnpj.com.br"
        # Captura as configurações estritas do Pydantic (fail-fast)
        self.token = settings.CPFCNPJ_API_TOKEN
        self.cpf_package = settings.CPFCNPJ_CPF_PACKAGE
        self.cnpj_package = settings.CPFCNPJ_CNPJ_PACKAGE

    async def consultar_cpf(self, cpf: str) -> Dict[str, Any]:
        """Consulta dados de CPF na API externa (Pacote B)."""
        url = f"{self.base_url}/{self.token}/{self.cpf_package}/{cpf}"
        return await self._make_request(url)

    async def consultar_cnpj(self, cnpj: str) -> Dict[str, Any]:
        """Consulta dados de CNPJ na API externa."""
        url = f"{self.base_url}/{self.token}/{self.cnpj_package}/{cnpj}"
        return await self._make_request(url)

    async def _make_request(self, url: str) -> Dict[str, Any]:
        """
        Método interno para padronizar as requisições, timeouts 
        e o parse dos erros HTTP para exceções de negócio.
        """
        try:
            # RNF01: Limite de tempo para não travar nossa API se a Receita Federal cair
            response = await self.http_client.get(url, timeout=10.0)
            
            # Tratamento focado nas respostas mapeadas da API cpfcnpj.com.br
            if response.status_code == 404:
                raise InvalidDocumentException("Documento não encontrado ou inválido na base da Receita.")
            
            if response.status_code in (402, 403):
                raise InsufficientCreditsException("Créditos insuficientes ou token de acesso inválido.")
                
            # Dispara exceção para outros códigos de erro (500, 502, 503...)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                raise InvalidDocumentException("A API retornou uma resposta em branco.")
                
            return data

        except httpx.TimeoutException:
            raise APITimeoutException("A API externa demorou muito para responder (Timeout).")
        except httpx.HTTPStatusError as e:
            raise APIUnavailableException(f"Erro na API externa: status {e.response.status_code}")
        except httpx.RequestError:
            raise APIUnavailableException("Falha de conexão física com a rede da API externa.")