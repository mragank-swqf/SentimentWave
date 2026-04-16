from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a transcript segmentation tool for earnings calls.
Split the transcript into segments where each segment is one speaker on one topic.

Rules:
- 3 to 12 sentences per segment
- Give each a topic_label as a short phrase e.g. "fuel cost outlook"
- role must be one of: CEO, CFO, CMD, Analyst, Operator, Other

Return ONLY a valid JSON array. 
Do not include any text before or after the JSON.
Do not include multiple JSON arrays.
No explanation, no markdown, no code fences.

Schema:
[{"segment_id":1,"speaker":"name","role":"CEO","text":"...","topic_label":"..."}]
"""

def safe_parse(text: str):
    matches = re.findall(r'\[.*?\]', text, re.DOTALL)
    if not matches:
        raise ValueError(f"No JSON array found: {text[:200]}")
    merged = []
    for m in matches:
        merged.extend(json.loads(m))
    return merged

def segment_transcript(raw_text: str) -> list[dict]:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.2
    )

    text = response.choices[0].message.content
    segments = safe_parse(text)
    return segments