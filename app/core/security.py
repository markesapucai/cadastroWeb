from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from passlib.context import CryptContext
from jose import jwt, JWTError

class JWTHandler:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(self, subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(days=7))
        to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise ValueError("Token inválido ou expirado")