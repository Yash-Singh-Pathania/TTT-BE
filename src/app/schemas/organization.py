from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationRead(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None

class OrganizationDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime
