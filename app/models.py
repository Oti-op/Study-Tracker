from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class StudySession(SQLModel, table=True):
    subject_id: Optional[int] = Field(default=None, primary_key=True)
    subject: str
    duration: int  # in minutes
    start_time: datetime
    