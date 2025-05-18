from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    message: str

class NotificationRead(BaseModel):
    id: int
    user_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True 