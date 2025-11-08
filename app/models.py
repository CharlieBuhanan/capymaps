from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Capybara(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job: str
    location: list[int]
    expiry_time: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    user: User
