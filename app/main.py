# import os

# from fastapi import FastAPI
# from models import Capybara
# from datetime import datetime
# from typing import Optional
# from sqlmodel import SQLModel, Field

# app = FastAPI()

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
    
# @app.get("/")
# async def read_root():
#         return {"message": "Hello, World!"}
# @app.post("capybara/place/")
# def place_capybara(capy: , x: int, y: int):
    # capy.placeCapy(x, y)

    # return

# @app.delete("capybara/{id}/")

# @app.get("/map/refresh/")

from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import Session
from db import init_db, get_session
from crud import create_capy, get_active_capys, delete_capy
from models import Capy, CapyCreate

app = FastAPI(title="Campus Capy Map 🐹")

@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/capys/", response_model=Capy)
def post_capy(capy_data: CapyCreate, session: Session = Depends(get_session)):
    capy = create_capy(session, capy_data)
    return capy


@app.get("/capys/", response_model=List[Capy])
def list_active_capys(session: Session = Depends(get_session)):
    return get_active_capys(session)


@app.delete("/capys/{capy_id}")
def remove_capy(capy_id: str, session: Session = Depends(get_session)):
    success = delete_capy(session, capy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Capy not found")
    return {"ok": True}
