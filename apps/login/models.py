from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
    sub: EmailStr
    

class TokenData(BaseModel):
    email: EmailStr
    