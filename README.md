# Chat Backend API

A simple messaging backend built using FastAPI and SQLite.

## Features

- Create users
- Send messages between users
- Retrieve conversation between two users

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy

## API Endpoints

POST /users  
GET /users  

POST /messages  

GET /messages/{user1}/{user2}

## How to Run

Install dependencies:

pip install fastapi uvicorn sqlalchemy

Run server:

uvicorn main:app --reload

Open API docs:

http://127.0.0.1:8000/docs
