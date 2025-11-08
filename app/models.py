from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str  # hashed password

class CapybaraMarker(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    x_coord: float
    y_coord: float
    activity: str  
    expires_at: datetime

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    title: str
    description: str
    x_coord: float
    y_coord: float
    time: datetime
    end_time: datetime
