from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    status,
    Body,
    Path,
    Query,
)
from fastapi.responses import JSONResponse
from sqlmodel import select, func
from uuid import UUID, uuid4
from typing import Annotated

from apps.deps import SessionDep
from config.settings import settings
from apps.deps import get_current_user
from apps.users.models import (
    User,
    UserCreate,
    UserUpdate,
    UserList,
    UserPublic
)
from config.security import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"], )


@router.get("/", response_model=UserList)
def get_users(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
    skip: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
) -> UserList:
    limit = min(limit, settings.MAX_LIMIT)
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()
    users_statement = select(User).offset(skip).limit(limit)
    users = session.exec(users_statement).all()
    users_public = [UserPublic.model_validate(user) for user in users]
    return UserList(items=users_public, total_count=count)


@router.get("/{id}", response_model=UserPublic)
def get_user(
    session: SessionDep,
    id: Annotated[UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserPublic:
    req_user = session.get(User, id)
    if not req_user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    user_public = UserPublic.model_validate(req_user)
    return user_public


@router.post("/", response_model=UserPublic)
def create_user(
    session: SessionDep,
    user_in: Annotated[UserCreate, Body()],
) -> UserPublic:
    if session.exec(select(User).where((User.email == user_in.email))).first():
        raise HTTPException(detail="User with same email or username already exists", status_code=status.HTTP_409_CONFLICT)
    data = user_in.model_dump()
    user = User(
        id=uuid4(),
        hashed_password=get_password_hash(data.pop("password")),
        **data
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user_public = UserPublic.model_validate(user)
    return user_public


@router.put("/{id}", response_model=UserPublic)
def update_user(
    session: SessionDep,
    user_in: Annotated[UserUpdate, Body()],
    id: Annotated[UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserPublic:
    user = session.get(User, id)
    if not user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    if user.id != current_user.id:
        raise HTTPException(detail="Not enough permission", status_code=status.HTTP_400_BAD_REQUEST)
    update_dict = user_in.model_dump(exclude_unset=True)
    user.sqlmodel_update(update_dict)
    session.add(user)
    session.commit()
    session.refresh(user)
    user_public = UserPublic.model_validate(user)
    return user_public


@router.delete("/{id}")
def delete_user(
    session: SessionDep,
    id: Annotated[UUID, Path()],
    current_user: Annotated[User, Depends(get_current_user)]
) -> JSONResponse:
    user = session.get(User, id)
    if not user:
        raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
    session.delete(user)
    session.commit()
    return JSONResponse(content={"detail": "User was successfully deleted"}, status_code=status.HTTP_200_OK)