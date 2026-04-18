from agents.scorer import score_segment

sample_segment = {
    "segment_id": 2,
    "speaker": "CFO Ramesh Babu",
    "role": "CFO",
    "text": "Fuel costs have increased approximately 8 percent this quarter. We believe this is a temporary situation subject to international coal price movements. We are exploring long-term fuel supply agreements to stabilize costs going forward.",
    "topic_label": "fuel cost outlook"
}

result = score_segment(sample_segment)
print(result)