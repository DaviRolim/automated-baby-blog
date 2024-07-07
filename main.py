from dotenv import load_dotenv

from services.baby_blog import create_blog_post
from services.baby_blog_crew import BabyBlogCrew
load_dotenv()

import asyncpg
import datetime
from fastapi import FastAPI
from pydantic import BaseModel

class CreateBlogRequest(BaseModel):
    topic: str

app = FastAPI()
crew = BabyBlogCrew()


@app.on_event("startup")
async def startup_event():
    conn = await asyncpg.connect('postgresql://postgres:postgres@db:5432/testdb')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS posts(
            id serial PRIMARY KEY,
            title text,
            image_url text,
            content text,
            created_at date
        )
    ''')

    # Insert a record into the created table.
    # await conn.execute('''
    #     INSERT INTO users(name, dob) VALUES($1, $2)
    # ''', 'James', datetime.date(1984, 3, 1))

    # # Select a row from the table.
    # row = await conn.fetchrow(
    #     'SELECT * FROM users WHERE name = $1', 'Bob')
    # # *row* now contains
    # # asyncpg.Record(id=1, name='Bob', dob=datetime.date(1984, 3, 1))
    # print(row)

    # Close the connection.
    await conn.close()

@app.get("/")
async def root():
    return {"message": "Hi, from fastAPI"}

@app.post("/")
async def new_blog_post(request: CreateBlogRequest):
    await create_blog_post(request.topic, crew)
    return {"message": "Blog post created"}