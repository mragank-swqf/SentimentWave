from agents.analyst import analyze_segments

sample_scored = [
    {"segment_id": 1, "speaker": "CMD Gurdeep Singh", "role": "CMD",
     "text": "Total generation reached 92 billion units.", "topic_label": "Q3 performance",
     "sentiment_score": 0.7, "tone": "bullish", "hedging_phrases": []},
    {"segment_id": 2, "speaker": "CFO Ramesh Babu", "role": "CFO",
     "text": "Fuel costs increased approximately 8 percent.", "topic_label": "fuel cost outlook",
     "sentiment_score": -0.3, "tone": "cautious", "hedging_phrases": ["we believe", "approximately"]}
]

result = analyze_segments(sample_scored)
print(result)