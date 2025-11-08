from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enums import ActivityEnum

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str  # hashed password
    instagram: Optional[str] = None

class CapybaraMarker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    x_coord: float
    y_coord: float
    activity: ActivityEnum  
    expires_at: datetime

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    title: str
    host: str
    description: str
    x_coord: float
    y_coord: float
    location: str
    time: datetime
    end_time: datetime
