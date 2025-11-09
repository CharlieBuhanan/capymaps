from datetime import datetime
from sqlmodel import Session, select
from scrapeCoords import EventPrototype, normalizeCoords, scanCapyEvents
from db import get_session, engine
from models import Event  # your existing SQLModel table class


def insert_events_to_existing_db(events: list[EventPrototype]):
    """Insert parsed EventPrototype objects into existing SQLModel table 'event'."""
    with get_session() as session:
        for ev in events:
            new_event = Event(
                id=ev.id,
                user_id=-1,  # assuming -1 for system/userless events
                title=ev.title,
                host=ev.host,
                description=ev.description,
                location=ev.location,
                x_coord=ev.x_coord,
                y_coord=ev.y_coord,
                time=ev.time,
                end_time=ev.end_time,
            )
            """existing = session.exec(select(Event).where(Event.title == ev.title, Event.time == ev.time)).first()
            if existing:
                continue  # skip duplicates"""
            session.add(new_event)

        # Commit inside the 'with' block, while session is open
        session.commit()

    print(f"Inserted {len(events)} events into 'event' table in capy.db.")

def deleteEvent(event_id: int):
    """Delete an event from the database by its ID."""
    with get_session() as session:
        event = session.get(Event, event_id)
        if event:
            session.delete(event)
            session.commit()
            print(f"Deleted event with ID {event_id}.")
        else:
            print(f"No event found with ID {event_id}.")

def select():
    #TODO implement select
    pass

def main():
    """for i in range(3, 204):
        deleteEvent(i)
    events = scanCapyEvents(100000)
    insert_events_to_existing_db(events)"""

if __name__ == "__main__":
    main()