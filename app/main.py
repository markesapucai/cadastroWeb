from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.routers import auth, queries, dashboard, reports

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Plataforma de consultas cadastrais com conformidade LGPD.",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ajustar em produção para os domínios corretos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montando a pasta de arquivos estáticos (CSS/JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluindo as rotas
app.include_router(auth.router)
app.include_router(queries.router)
app.include_router(dashboard.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao CadastroWeb API"}