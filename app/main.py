import os

from fastapi import FastAPI
from models import Capybara, User
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

app = FastAPI()

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    

@app.post("capybara/place/")
def place_capybara(capy: Capy, x: int, y: int):
    capy.placeCapy(x, y)

    return

@app.delete("capybara/{id}/")

@app.get("/map/refresh/")

