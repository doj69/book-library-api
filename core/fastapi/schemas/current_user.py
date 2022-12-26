from typing import Optional
from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: Optional[int] = None

    class Config:
        validate_assignment = True
