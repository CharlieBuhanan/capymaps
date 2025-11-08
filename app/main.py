from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from datetime import datetime
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
)
from auth import create_access_token, get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mapybara")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    asyncio.create_task(cleanup_task())
    yield

app = FastAPI(title="Mapybara", lifespan=lifespan)

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

# -------------------------------------
# Cleanup Task to remove Dead Capybaras
# -------------------------------------

async def cleanup_task():
    """Periodically delete expired markers every 30 minutes."""
    while True:
        try:
            await asyncio.sleep(1800)  # 30 minutes
            with Session(engine) as session:
                deleted = delete_expired_markers(session, datetime.now())
                if deleted:
                    logger.info(f"[Cleanup] Removed {deleted} expired capybaras at {datetime.now()}")
        except Exception as e:
            logger.error(f"[Cleanup] Error during cleanup: {e}")

