from pydantic import BaseModel, model_validator
from datetime import datetime
from enums import ActivityEnum

class UserCreate(BaseModel):
    username: str
    password: str
    instagram: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class CapybaraMarkerCreate(BaseModel):
    x_coord: float
    y_coord: float
    activity: ActivityEnum

class EventCreate(BaseModel):
    title: str
    description: str
    x_coord: float
    y_coord: float
    time: datetime
    end_time: datetime
    host: str
    location: str

    @model_validator(mode="after")
    def check_time(cls, values):
        start, end = values.time, values.end_time
        if end <= start:
            raise ValueError("end_time must be after start time")
        return values

class Token(BaseModel):
    access_token: str
    token_type: str
