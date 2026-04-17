from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from db_models import Transcript, Segment, Analysis
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UploadRequest(BaseModel):
    ticker: str
    company_name: str
    quarter: int
    year: int
    text: str

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/upload")
def upload_transcript(req: UploadRequest, db: Session = Depends(get_db)):
    transcript = Transcript(
        ticker=req.ticker,
        company_name=req.company_name,
        quarter=req.quarter,
        year=req.year,
        raw_text=req.text
    )
    db.add(transcript)
    db.commit()
    db.refresh(transcript)
    return {"transcript_id": transcript.id}

from agents.segmenter import segment_transcript

@app.post("/analyze/{transcript_id}")
def analyze(transcript_id: int, db: Session = Depends(get_db)):
    transcript = db.query(Transcript).filter(
        Transcript.id == transcript_id
    ).first()
    
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    # Agent 1
    segments = segment_transcript(transcript.raw_text)
    
    # Save segments to DB (scores will be filled in by Agent 2 tomorrow)
    for i, seg in enumerate(segments):
        db_segment = Segment(
            transcript_id=transcript.id,
            segment_index=i,
            speaker=seg.get("speaker"),
            role=seg.get("role"),
            text=seg.get("text"),
            topic_label=seg.get("topic_label")
        )
        db.add(db_segment)
    
    db.commit()
    return {
        "message": "Segmentation complete",
        "transcript_id": transcript_id,
        "segment_count": len(segments)
    }