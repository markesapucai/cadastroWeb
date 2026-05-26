from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "CadastroWeb"
    
    # Database
    DATABASE_URL: str
    
    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CPF.CNPJ API
    CPFCNPJ_API_TOKEN: str
    CPFCNPJ_CPF_PACKAGE: int = 1  # Pacote B por padrão
    CPFCNPJ_CNPJ_PACKAGE: int = 1
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()