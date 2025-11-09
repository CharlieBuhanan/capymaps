from fastapi import Body, FastAPI, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from sqlalchemy import desc
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import asyncio
import logging

from db import init_db, get_session, engine
from models import CapybaraMarker, Event, User
from schemas import UserCreate, UserLogin, CapybaraMarkerCreate, EventCreate, Token
from crud import (
    create_user,
    authenticate_user,
    create_marker,
    create_event,
    delete_expired_markers,
    delete_finished_events,
)
from auth import create_access_token, get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mapybara")


app = FastAPI(title="Mapybara")

bearer_scheme = HTTPBearer()

def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    return get_current_user(token=token, session=session)

# ----------------------------
# User Registration and Login 
# ----------------------------

@app.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(session, user)

@app.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = authenticate_user(session, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/{username}/history")
def get_user_history(username: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    markers = session.exec(
    select(CapybaraMarker)
    .where(CapybaraMarker.user_id == user.id)
    .order_by(desc(CapybaraMarker.expires_at)) # type: ignore
).all()


    history = []
    for m in markers:
        time_posted = m.expires_at - timedelta(hours=4)
        history.append({
            "x_coord": m.x_coord,
            "y_coord": m.y_coord,
            "activity": m.activity,
            "time_posted": time_posted,
        })

    return {
        "user": {
            "username": user.username,
            "instagram": user.instagram,
        },
        "history": history,
    }

# ----------------
# Capybara Markers
# ----------------

@app.post("/markers")
def add_marker(
    marker: CapybaraMarkerCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user_from_token),
):
    return create_marker(session, marker, user_id=current_user.id)

@app.get("/markers")
def get_markers(session: Session = Depends(get_session)):
    return session.exec(select(CapybaraMarker)).all()

@app.put("/markers/{id}")
def update_marker(
    id: int,
    marker_update: CapybaraMarkerCreate = Body(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token),
):
    capy = session.get(CapybaraMarker, id)
    if not capy:
        raise HTTPException(status_code=404, detail="Capy not found")
    if capy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this capy")
    
    reset_timer = False

    if (capy.x_coord != marker_update.x_coord):
        capy.x_coord = marker_update.x_coord
        reset_timer = True

    if (capy.y_coord != marker_update.y_coord):
        capy.y_coord = marker_update.y_coord
        reset_timer = True

    if (capy.activity != marker_update.activity):
        capy.activity = marker_update.activity
        reset_timer = True

    if reset_timer:
        capy.expires_at = datetime.now() + timedelta(hours=4)

    session.add(capy)
    session.commit()
    session.refresh(capy)
    return capy
        

@app.delete("/markers/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_marker(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token),
):
    capy = session.get(CapybaraMarker, id)
    if not capy:
        raise HTTPException(status_code=404, detail="Capy not found")
    if capy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this capy")
    
    session.delete(capy)
    session.commit()
    return None

# --------------
# Events Markers
# --------------

@app.post("/events")
def add_event(
    event: EventCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user_from_token),
):
    return create_event(session, event, user_id=current_user.id)

@app.get("/events")
def get_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()

@app.put("/events/{event_id}")
def update_event(
    event_id: int,
    event_update: EventCreate = Body(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    
    update_data = event_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if getattr(event, field) != value:
            setattr(event, field, value)

    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@app.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    
    session.delete(event)
    session.commit()
    return None

# ---------------------------------------------------------
# Cleanup Task to remove Dead Capybaras and Finished Events
# ---------------------------------------------------------

async def cleanup_task(stop_event: asyncio.Event):
    """Periodically delete expired markers every 30 minutes."""
    while not stop_event.is_set():
        try:
            await asyncio.sleep(1800)
            with Session(engine) as session:
                deleted_markers = delete_expired_markers(session, datetime.now())
                deleted_events = delete_finished_events(session, datetime.now())
                if deleted_markers or deleted_events:
                    logger.info(f"[Cleanup] Removed {deleted_markers} markers and {deleted_events} events")
        except Exception as e:
            logger.error(f"[Cleanup] Error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    stop_event = asyncio.Event()
    task = asyncio.create_task(cleanup_task(stop_event))
    logger.info("Background cleanup task started.")
    yield
    stop_event.set()
    task.cancel()
    logger.info("Background cleanup task stopped.")

