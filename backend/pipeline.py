from agents.segmenter import segment_transcript
from agents.scorer import score_segment
from agents.analyst import analyze_segments

def run_pipeline(raw_text:str)->dict:
    segments = segment_transcript(raw_text)

    scored_segments = []
    for seg in segments:
        score = score_segment(seg)
        scored_segments.append({
            **seg,                    ##seg is a dictionary,thus **seg
            "sentiment_score":score.get("sentiment_score"),
            "tone":score.get("tone"),
            "hedging_phrase": score.get("hedging_phrases", [])
        })

        analysis = analyze_segments(scored_segments)

        return {
            "segments":scored_segments,
            "analysis":analysis
        }