# from sqlmodel import SQLModel, Field
# from datetime import datetime
# from typing import Optional

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str
#     email: str
#     created_at: datetime = Field(default_factory=datetime.utcnow)

# class Capybara(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     job: str
#     location: list[int]
#     expiry_time: datetime
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     user_id: int = Field(foreign_key="user.id")
#     user: User

from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
# from typing import Optional
import uuid


class Capy(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    activity: str
    latitude: float
    longitude: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.expires_at


# Request schema (optional, could use Capy directly)
class CapyCreate(SQLModel):
    name: str
    activity: str
    latitude: float
    longitude: float
    duration_minutes: int = 60  # how long until expiration
