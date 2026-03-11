# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from models import TodoItem
from database import db
from services import add_todo

app = FastAPI()

@app.get("/")
async def home(todo_items: TodoItem):
    return {todo_items: TodoItem.parse_obj(todo_items)}

# models.py
from typing import List

class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool = False
    
    class Config:
        allow_mutation = False

# database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from models import TodoItem

engine = create_engine(f'sqlite:///{TodoItem.DATABASE_URI}')
Session = sessionmaker(bind=engine)
db_session = Session()

# services.py
@app.post("/add_todo", response_model=TodoItem)
async def add_todo(title: str, completed: bool = False) -> TodoItem:
    todo_item = TodoItem(title=title, completed=completed)
    db_session.add(todo_item)
    db_session.commit()
    return todo_item

# requirements.txt
pydantic==2.7.2
fastapi==3.8.5
asyncpg-asyncio==1.11.0
aiohttp==4.0.2