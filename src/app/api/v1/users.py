from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from ...core.db.database import async_get_db
from ...core.security import get_password_hash, verify_password
from ...models.user import User
from ...schemas.user import UserCreate, UserRead, UserCreateInternal
from ...crud.crud_users import crud_users

router = APIRouter(tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup", response_model=UserRead, status_code=201)
async def signup(
    user: UserCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> UserRead:
    async with db.begin():
        try:
            # Check for duplicate email
            stmt = select(User).filter_by(email=user.email)
            result = await db.execute(stmt)
            if result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already registered",
                )
            
            # Create user
            user_internal_dict = user.model_dump()
            user_internal_dict["hashed_password"] = get_password_hash(user.password)
            del user_internal_dict["password"]

            user_internal = UserCreateInternal(**user_internal_dict)
            new_user = User(**user_internal.dict())
            
            db.add(new_user)
            await db.commit()

            return user_internal

        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error processing request",
            )

@router.post("/login")
async def login():
    # Placeholder for the login endpoint
    return {"message": "Login endpoint not implemented yet"}
