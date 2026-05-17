from pydantic import BaseModel, Field
from datetime import datetime

class sessioncreate(BaseModel):
    subject: str
    duration: int = Field(gt=0)
    start_time: datetime

class sessionread(BaseModel):
    subject_id: int
    subject: str
    duration: int
    start_time: datetime
    model_config = {"from_attributes": True}

