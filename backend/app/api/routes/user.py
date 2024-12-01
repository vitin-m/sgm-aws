from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.core import crud
from app.core.models import UserCreate, UserPublic, UserUpdate

router = APIRouter()


@router.post("/signup", response_model=UserPublic)
async def register_user(session: SessionDep, user_in: UserCreate) -> UserPublic:
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail="User credential already registered"
        )
    user_create = UserCreate.model_validate(user_in)
    user = crud.create_user(session=session, user_create=user_create)
    return UserPublic.model_validate(user)


@router.get("/me")
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.patch("/me")
async def update_user_me(
    *, session: SessionDep, user_in: UserUpdate, current_user: CurrentUser
):
    if user_in.email:
        user = crud.get_user_by_email(session=session, email=user_in.email)
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User credential already registered"
            )

    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
