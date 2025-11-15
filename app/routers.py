from fastapi import APIRouter, HTTPException
from sqlomdel import Session, select
from typing import List, Optional
from datetime import datetime

from app.models import StudySession
from app.schemas import sessioncreate, sessionread
from app.database import engine

router = APIRouter(prefix="/sessions", tags=["study sessions"])

@router.post("/", response_model=sessionread, status_Code=201)
def create_session(session: sessioncreate):
    with Session(engine) as db:
        db_session = StudySession(
            subject=session.subject,
            duration=session.duration,
            start_time=session.start_time 
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
@router.get("/", response_model=List[sessionread])
def list_sessions(subject: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    stmt = select(StudySession)

    if subject:
        stmt = stmt.where(StudySession.subject == subject)
    if start_date:
        stmt = stmt.where(StudySession.start_time >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        stmt = stmt.where(StudySession.start_time <= datetime.combine(end_date, datetime.max.time()))

        with Session(engine) as db:
            results = db.exec(stmt).all()
            return results
        
@router.get("/{subject_id}", response_model=sessionread)
def get_session(subject_id: int):
    with Session(engine) as db:
        session = db.get(StudySession, subject_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session