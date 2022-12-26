from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int]
    password: Optional[str]
    email: Optional[str]
    nickname: Optional[str]
    is_admin: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
