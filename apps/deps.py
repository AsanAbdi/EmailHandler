from collections.abc import Generator
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
from sqlmodel import Session, select

from config.settings import settings
from apps.users.models import User
from config.security import ALGORITHM
from config.db import engine


scheme_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)



def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

def get_current_user(
    session: SessionDep,
    token: str = Depends(scheme_oauth2)
) -> User:
    exception = HTTPException(
        detail="Invalid token provided",
        status_code=status.HTTP_400_BAD_REQUEST
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, ALGORITHM) #type: ignore
        user_email = payload.get("sub") #type: ignore
        if not user_email:
            raise exception
    except jwt.PyJWTError: #type: ignore
        raise exception
    
    user = session.exec(select(User).where(User.email == user_email)).first() #type: ignore
    if not user:
        raise exception
    return user 