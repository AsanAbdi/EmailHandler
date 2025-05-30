from passlib.context import CryptContext
from datetime import timedelta
from typing import Any
import jwt

from apps.login.models import TokenData
from config.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_token(subject: str, expires_delta: timedelta) -> Any:
    expire = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = {"expire": expire, "sub": str(subject)} #type: ignore
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM) # type: ignore
    return encoded_jwt #type: ignore

def verify_token(
    token: str,
) -> TokenData | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, ALGORITHM) #type: ignore
        sub = payload.get("sub") #type: ignore
        if sub is None:
            return None
        
        return TokenData(username=sub) #type: ignore
    except jwt.PyJWTError: #type: ignore
        return None
