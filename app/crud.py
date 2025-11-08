from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from models import Capy, CapyCreate

def create_capy(session: Session, capy_data: CapyCreate) -> Capy:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=capy_data.duration_minutes)
    capy = Capy(
        name=capy_data.name,
        activity=capy_data.activity,
        latitude=capy_data.latitude,
        longitude=capy_data.longitude,
        expires_at=expires_at,
    )
    session.add(capy)
    session.commit()
    session.refresh(capy)
    return capy


def get_active_capys(session: Session):
    now = datetime.now(timezone.utc)
    statement = select(Capy).where(Capy.expires_at > now)
    return session.exec(statement).all()


def delete_capy(session: Session, capy_id):
    capy = session.get(Capy, capy_id)
    if not capy:
        return None
    session.delete(capy)
    session.commit()
    return True
