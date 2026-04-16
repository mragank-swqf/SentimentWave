from agents.segmenter import segment_transcript

sample = """
Operator: Good morning. Welcome to NTPC's Q3 earnings call.

CMD Gurdeep Singh: Thank you. I am pleased to report that our total generation 
reached 92 billion units this quarter, a 6 percent increase year on year. 
Our coal-based plants operated at a plant load factor of 74 percent. 
We remain committed to our renewable energy targets.

Analyst: Can you speak to the rising fuel costs and how that impacts margins?

CFO Ramesh Babu: Fuel costs have increased approximately 8 percent this quarter. 
We believe this is a temporary situation subject to international coal price movements. 
We are exploring long-term fuel supply agreements to stabilize costs going forward.
"""

segments = segment_transcript(sample)
for s in segments:
    print(s)
    print("---")