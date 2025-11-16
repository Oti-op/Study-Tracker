from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from datetime import datetime, date
import matplotlib.pyplot as plt
import io

from app.models import StudySession
from app.database import engine

router = APIRouter(prefix="/charts", tags=["charts"])

@router.get("/progress.png")
def stude_progress_chart(
    subject: str | None = Query(None),
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
):
    stmt = select(StudySession)

    if subject:
        stmt = stmt.where(StudySession.subject == subject)
    if from_date:
        stmt = stmt.where(StudySession.start_time >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        stmt = stmt.where(StudySession.start_time <= datetime.combine(to_date, datetime.max.time()))

    with Session(engine) as db:
            rows = db.exec(stmt).all()    

    if not rows:
         plt.figure(figsize=(6, 3))
         plt.text(0.5, 0.5, "no data", ha="center", va="center")
         plt.axis("off")
         buf = io.BytesIO()
         plt.savefig(buf, format="png", bbox_inches="tight")
         plt.close()
         buf.seek(0)
         return StreamingResponse(buf, media_type="image/png")
    
    totals = {}
    for r in rows:
         d = r.start_time.date()
         totals[d] = totals.get(d, 0) + r.duration

    dates = sorted(totals.keys())
    x = [d.strftime("%Y-%m-%d") for d in dates]
    y = [totals[d] for d in dates]

    plt.figure(figssize=(6, 3))
    plt.plot(x, y, marker="o")
    plt.xtricks(rotation=45)
    plt.xlabel("Dates")
    plt.ylabel("Minutes Studied")
    plt.title("Study Progress")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
