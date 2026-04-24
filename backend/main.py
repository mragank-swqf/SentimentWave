from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from db_models import Transcript, Segment, Analysis
import uvicorn
from agents.segmenter import segment_transcript
from agents.scorer import score_segment
from pipeline import run_pipeline
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


@app.post("/analyze/{transcript_id}")
def analyze(transcript_id: int, db: Session = Depends(get_db)):
    transcript = db.query(Transcript).filter(
        Transcript.id == transcript_id
    ).first()
    
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")
    
    result = run_pipeline(transcript.raw_text)
    
    for i, seg in enumerate(result["segments"]):
        score = score_segment(seg)
        db_segment = Segment(
            transcript_id=transcript.id,
            segment_index=i,
            speaker=seg.get("speaker"),
            role=seg.get("role"),
            text=seg.get("text"),
            topic_label=seg.get("topic_label"),
            sentiment_score = score.get("sentiment_score"),
            tone=score.get("tone"),
            hedging_phrases=score.get("hedging_phrases", [])
        )
        db.add(db_segment)
    
    analysis = result["analysis"]
    db_analysis = Analysis(
        transcript_id = transcript.id,
        overall_sentiment=analysis.get("overall_sentiment"),
        summary=analysis.get("summary"),
        notable_moments=analysis.get("notable_moments", [])
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return {
        "analysis_id" : db_analysis.id,
        "overall_sentiment" : db_analysis.overall_sentiment,
        "summary": db_analysis.summary,
        "notable_moments": db_analysis.notable_moments
    }