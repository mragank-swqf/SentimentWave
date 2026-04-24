from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a financial analyst summarizing an earnings call sentiment analysis.
You have all segments with sentiment scores and tones.

Tasks:
1. Write a 3-sentence plain English summary of management tone. No jargon.
2. Pick 3 most notable moments — unusual score, evasive tone, topic changes.
3. Set overall_sentiment as a float summary of the whole call.

Return ONLY valid JSON. No explanation, no markdown, no code fences.

Schema:
{"overall_sentiment": 0.2, "summary": "Management sounded cautious...", "notable_moments": [{"segment_id": 2, "reason": "CFO was evasive on fuel costs."}]}
"""

def safe_parse(text: str):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found: {text[:200]}")
    return json.loads(match.group())

def analyze_segments(scored_segments: list[dict])->dict:
    trimmed = [{
        "segment_id": s.get("segment_id"),
        "role": s.get("role"),
        "topic_label": s.get("topic_label"),
        "sentiment_score": s.get("sentiment_score"),
        "tone": s.get("tone")
    } for s in scored_segments]
    content = json.dumps(trimmed, indent=2)
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {"role":"system", "content": SYSTEM_PROMPT},
            {"role":"user", "content":content}
        ],
        temperature=0.2,
        max_tokens=2000
    )
    return safe_parse(response.choices[0].message.content)