from google import genai
import os, json, re
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are a financial sentiment scorer analyzing earnings call segments.
- sentiment_score: float from -1.0 to +1.0
- tone: one of bullish / cautious / neutral / defensive / evasive
- hedging_phrases: list exact phrases that soften or avoid commitment
Return ONLY valid JSON. No explanation, no markdown, no code fences.
Schema:
{"sentiment_score": 0.3, "tone": "cautious", "hedging_phrases": ["we believe", "approximately"]}
"""

def safe_parse(text: str):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found: {text[:200]}")
    return json.loads(match.group())

def score_segment(segment: dict) -> dict:
    content = f"Topic: {segment.get('topic_label')}\nRole: {segment.get('role')}\nText: {segment.get('text', '')}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{content}",
        config={"temperature": 0.2}
    )
    return safe_parse(response.text)