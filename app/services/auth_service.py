from app.repositories.user_repository import UserRepository
from app.core.security import JWTHandler
from app.models.user import User

class AuthenticationError(Exception):
    pass

class AuthService:
    def __init__(self, user_repo: UserRepository, jwt_handler: JWTHandler):
        self.user_repo = user_repo
        self.jwt_handler = jwt_handler

    async def authenticate_user(self, email: str, password: str) -> dict[str, str]:
        """
        Valida credenciais e retorna access e refresh tokens.
        """
        user = await self.user_repo.get_by_email(email)
        
        if not user or not user.is_active:
            raise AuthenticationError("Credenciais inválidas ou usuário inativo.")
            
        if not self.jwt_handler.verify_password(password, user.hashed_password):
            raise AuthenticationError("Credenciais inválidas.")
            
        access_token = self.jwt_handler.create_access_token(subject=user.id)
        refresh_token = self.jwt_handler.create_refresh_token(subject=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }