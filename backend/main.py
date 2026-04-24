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

@app.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    segments = db.query(Segment).filter(
        Segment.transcript_id == analysis.transcript_id
    ).order_by(Segment.segment_index).all()

    return {
        "analysis_id": analysis.id,
        "transcript_id": analysis.transcript_id,
        "overall_sentiment": analysis.overall_sentiment,
        "summary": analysis.summary,
        "notable_moments": analysis.notable_moments,
        "created_at": str(analysis.created_at),
        "segments": [
            {
                "segment_index": s.segment_index,
                "speaker": s.speaker,
                "role": s.role,
                "text": s.text,
                "topic_label": s.topic_label,
                "sentiment_score": s.sentiment_score,
                "tone": s.tone,
                "hedging_phrases": s.hedging_phrases
            } for s in segments
        ]
    }

@app.get("/waveform/{transcript_id}")
def get_waveform(transcript_id: int, db: Session = Depends(get_db)):
    segments = db.query(Segment).filter(
        Segment.transcript_id == transcript_id
    ).order_by(Segment.segment_index).all()

    if not segments:
        raise HTTPException(status_code=404, detail="No segments found")
    return [
        {
            "segment_index": s.segment_index,
            "sentiment_score": s.sentiment_score,
            "topic_label": s.topic_label,
            "tone": s.tone,
            "speaker": s.speaker
        } for s in segments
    ]

@app.get("/transcripts")
def get_transcripts(db: Session = Depends(get_db)):
    transcripts = db.query(Transcript).order_by(
        Transcript.uploaded_at.dec()
    ).all()
    return [
        {
            "id": t.id,
            "ticker": t.ticker,
            "company_name": t.company_name,
            "quarter": t.quarter,
            "year": t.year,
            "uploaded_at": str(t.uploaded_at)
        } for t in transcripts
    ]