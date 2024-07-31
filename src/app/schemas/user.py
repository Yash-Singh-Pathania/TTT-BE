from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field
from enum import Enum

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_HEAD = "org_head"
    PLAYER = "player"

class UserBase(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=30, examples=["User"])]
    last_name: Annotated[str, Field(min_length=2, max_length=30, examples=["Userson"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"])]
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]


class User(TimestampSchema, UserBase, UUIDSchema, PersistentDeletion):
    profile_image_url: Annotated[str, Field(default="https://www.profileimageurl.com")]
    hashed_password: str
    role: UserRole
    organization_id: int
    is_superuser: bool = False

class UserRead(BaseModel):
    id: int
    first_name: Annotated[str, Field(min_length=2, max_length=30, examples=["User"])]
    last_name: Annotated[str, Field(min_length=2, max_length=30, examples=["Userson"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"])]
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]
    profile_image_url: str
    role: UserRole
    organization_id: int

class UserCreate(UserBase):
    password: Annotated[str, Field(examples=["Yash7150"])]

class UserCreateInternal(UserBase):
    hashed_password: str
    role: UserRole
    organization_id: int

class UserUpdate(BaseModel):
    first_name: Annotated[str | None, Field(min_length=2, max_length=30, examples=["User"], default=None)]
    last_name: Annotated[str | None, Field(min_length=2, max_length=30, examples=["Userberg"], default=None)]
    username: Annotated[str | None, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userberg"], default=None)]
    email: Annotated[EmailStr | None, Field(examples=["user.userberg@example.com"], default=None)]
    profile_image_url: Annotated[str | None, Field(pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.profileimageurl.com"], default=None)]

class UserUpdateInternal(UserUpdate):
    hashed_password: str | None
    updated_at: datetime

class UserTierUpdate(BaseModel):
    organization_id: int

class UserDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime

class UserRestoreDeleted(BaseModel):
    is_deleted: bool
