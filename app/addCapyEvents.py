from datetime import datetime
from sqlmodel import Session, select
from scrapeCoords import EventPrototype
from db import get_session, engine
from models import Event, CapybaraMarker  # your existing SQLModel table class

#THESE DO NOT WORK IF @contextmanager IS NOT USED IN db.py FOR get_session(). REVERT WHEN NOT IN USE.
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

def deleteCapy(capy_id: int):
    """Delete an event from the database by its ID."""
    with get_session() as session:
        capy = session.get(CapybaraMarker, capy_id)
        if capy:
            session.delete(capy)
            session.commit()
            print(f"Deleted event with ID {capy_id}.")
        else:
            print(f"No event found with ID {capy_id}.")

def selectEvent(event_id: int):
    with get_session() as session:
        event = session.get(Event, event_id)
        if event:
            #print(f"Event ID: {event.id}, Title: {event.title}, Time: {event.time}")
            eventList = [event.id, event.title, event.host, event.description, event.x_coord, event.y_coord, event.location, event.time, event.end_time]
            return eventList
        else:
            print(f"No event found with ID {event_id}.")

def main():
    for i in range(4, 39):
        deleteCapy(i)

    """for i in range(3, 204):
        deleteEvent(i)
    events = scanCapyEvents(100000)
    insert_events_to_existing_db(events)"""

if __name__ == "__main__":
    main()