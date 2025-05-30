from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserCreate(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = Field(max_length=255)


class UserPublic(SQLModel):
    id: UUID
    email: EmailStr


class UserList(SQLModel):
    items: list[UserPublic]
    total_count: int


class User(SQLModel, table=True):
    __tablename__ = "user" #type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, unique=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
