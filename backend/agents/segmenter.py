from google import genai
import os, json, re
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a transcript segmentation tool for earnings calls.
Split the transcript into segments where each segment is one speaker on one topic.
Rules:
- 3 to 12 sentences per segment
- Give each a topic_label as a short phrase e.g. "fuel cost outlook"
- role must be one of: CEO, CFO, CMD, Analyst, Operator, Other
Return ONLY a valid JSON array. No text before or after. No markdown.
Schema:
[{"segment_id":1,"speaker":"name","role":"CEO","text":"...","topic_label":"..."}]
"""

def safe_parse(text: str):
    matches = re.findall(r'\[.*\]', text, re.DOTALL)
    if not matches:
        raise ValueError(f"No JSON array found: {text[:200]}")
    merged = []
    for m in matches:
        try:
            merged.extend(json.loads(m))
        except json.JSONDecodeError:
            continue
    return merged

def segment_transcript(raw_text: str) -> list[dict]:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{raw_text}",
        config={"temperature": 0.2}
    )
    return safe_parse(response.text)