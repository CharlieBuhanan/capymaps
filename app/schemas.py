from pydantic import BaseModel
from datetime import datetime

# Schema for Capybara (for validation and response)
class CapybaraBase(BaseModel):
    mood: str
    location_lat: float
    location_lng: float
    expiry_time: datetime

class CapybaraCreate(CapybaraBase):
    pass

class Capybara(CapybaraBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True  # This tells Pydantic to treat ORM models like dicts

# Schema for User (for validation and response)
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
