from fastapi import FastAPI, HTTPException
from app.database import create_db_and_tables
from app.routers import router as sessions_router

app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(sessions_router)