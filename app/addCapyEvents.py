from sqlmodel import SQLModel, Field, Relationship, create_engine, Session, select
from typing import Optional, List
from datetime import datetime
from scrapeCoords import EventPrototype, normalizeCoords, scanCapyEvents


# --- Your existing pieces assumed to exist ---
# - months list
# - EventPrototype class
# - normalizeCoords()
# - scanCapyEvents(n)



# --- Insert logic using the ORM ---

def get_or_create_location(session: Session, name: str):
    result = session.exec(select(Location).where(Location.name == name)).first()
    if result:
        return result
    coords = normalizeCoords(name)
    x, y = coords if coords else (-1, -1)
    loc = Location(name=name, x_coord=x, y_coord=y)
    session.add(loc)
    session.commit()
    session.refresh(loc)
    return loc


def get_or_create_host(session: Session, name: str):
    result = session.exec(select(Host).where(Host.name == name)).first()
    if result:
        return result
    host = Host(name=name)
    session.add(host)
    session.commit()
    session.refresh(host)
    return host


def insert_events_sqlmodel(events: list[EventPrototype], engine):
    """Convert EventPrototype objects into SQLModel Event objects and insert."""
    with Session(engine) as session:
        for ev in events:
            loc = get_or_create_location(session, ev.location)
            host = get_or_create_host(session, ev.host)
            event = Event(
                id=ev.id,
                title=ev.title,
                description=ev.description,
                time=ev.time,
                end_time=ev.end_time,
                location_id=loc.id,
                host_id=host.id,
            )
            session.add(event)
        session.commit()


# --- Main entry point ---

def main():
    engine = init_db("sqlite:///capyEvents.db")  # or any other DB URL
    events = scanCapyEvents(10)
    insert_events_sqlmodel(events, engine)
    print(f"Inserted {len(events)} events into SQLModel database.")


if __name__ == "__main__":
    main()