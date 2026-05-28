import asyncio
from app.core.database import SessionLocal, engine, Base
from app.core.security import JWTHandler
from app.core.config import settings
from app.repositories.user_repository import UserRepository

# IMPORTANTE: Precisamos importar os modelos aqui para que o SQLAlchemy saiba que eles existem
from app.models.user import User
from app.models.query_log import QueryLog

async def create_first_admin():
    print("🚀 Verificando e criando tabelas no banco de dados do Render...")
    
    # Esta linha se conecta ao banco e cria todas as tabelas (users, logs) se elas não existirem
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tabelas sincronizadas com sucesso!")

    print("👤 Iniciando criação do usuário administrador...")
    jwt_handler = JWTHandler(secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    email = "admin@empresarial.com"
    senha_pura = "SenhaMestra123!"
    senha_hasheada = jwt_handler.get_password_hash(senha_pura)
    
    async with SessionLocal() as session:
        user_repo = UserRepository(session)
        
        existing_user = await user_repo.get_by_email(email)
        if existing_user:
            print("⚠️ Usuário admin@empresarial.com já está cadastrado no banco!")
            return

        await user_repo.create(
            email=email,
            hashed_password=senha_hasheada,
            is_admin=True
        )
        
    print("\n" + "="*40)
    print("✅ Usuário criado com sucesso!")
    print(f"📧 E-mail: {email}")
    print(f"🔑 Senha: {senha_pura}")
    print("="*40 + "\n")

if __name__ == "__main__":
    asyncio.run(create_first_admin())