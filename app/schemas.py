from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from enums import ActivityEnum

class UserCreate(BaseModel):
    username: str
    password: str
    instagram: str | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        if " " in v:
            raise ValueError("Username cannot contain spaces")
        if not (3 <= len(v) <= 30):
            raise ValueError("Username must be between 3 and 30 characters long")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
            return v
        if len(v) > 128:
            raise ValueError("Password must not exceed 128 characters")
            return v
        return v

class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        if not (3 <= len(v) <= 30):
            raise ValueError("Invalid username length")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if not (8 <= len(v) <= 128):
            raise ValueError("Invalid password length")
        return v


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
