import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from app.database import create_db_and_tables
from app.routers.routers import router as sessions_router
from app.routers.chart import router as chart_router

app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(sessions_router)
app.include_router(chart_router)

BASEDIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASEDIR, "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
