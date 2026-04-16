from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Transcript, Segment, Analysis
import uvicorn

class UploadRequest(BaseModel):
    ticker: str
    company_name: str
    quarter: int
    year: int
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], #whitelist of allowed frontends
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"transcript_id":transcript.id}