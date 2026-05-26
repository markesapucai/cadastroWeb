from pydantic import BaseModel, Field

class DocumentQuery(BaseModel):
    document: str = Field(..., description="O CPF ou CNPJ a ser consultado, com ou sem pontuação")