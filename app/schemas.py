from pydantic import BaseModel, conint
from datetime import datetime

class sessioncreate(BaseModel):
    subject: str
    duration: conint(gt=0)  # duration must be a positive integer
    start_time: datetime

class sessionread(BaseModel):
    subject_id: int
    subject: str
    duration: int
    start_time: datetime
    class Config:
        orm_mode = True

