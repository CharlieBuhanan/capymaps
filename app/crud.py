from sqlmodel import Session, select
from datetime import datetime, timedelta
from models import User, CapybaraMarker, Event
from schemas import UserCreate, CapybaraMarkerCreate, EventCreate
from auth import hash_password, verify_password

# ----------------------------
# User Registration and Login 
# ----------------------------

def create_user(session: Session, user: UserCreate):
    db_user = User(username=user.username, password=hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def authenticate_user(session: Session, username: str, password: str):
    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user or not verify_password(password, db_user.password):
        return None
    return db_user

# ----------------
# Capybara Markers
# ----------------

def create_marker(session: Session, marker: CapybaraMarkerCreate, user_id: int):
    expires_at = datetime.now() + timedelta(hours=4)
    db_marker = CapybaraMarker(x_coord=marker.x_coord,
        y_coord=marker.y_coord,
        activity=marker.activity,
        user_id=user_id,
        expires_at=expires_at)
    session.add(db_marker)
    session.commit()
    session.refresh(db_marker)
    return db_marker

# --------------
# Events Markers
# --------------

def create_event(session: Session, event: EventCreate, user_id: int):
    db_event = Event(title=event.title,
        description=event.description,
        x_coord=event.x_coord,
        y_coord=event.y_coord,
        time=event.time,
        end_time=event.end_time,
        user_id=user_id,
        host=event.host,
        location=event.location)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

# -----------------------------------
# Terminate Dead Capybaras and Events
# -----------------------------------

def delete_expired_markers(session: Session, current_time: datetime):
    expired = session.exec(select(CapybaraMarker).where(CapybaraMarker.expires_at < current_time)).all()
    for marker in expired:
        session.delete(marker)
    session.commit()
    return len(expired)

def delete_finished_events(session: Session, current_time: datetime):
    finished = session.exec(select(Event).where(Event.end_time < current_time)).all()
    for event in finished:
        session.delete(event)
    session.commit()
    return len(finished)
