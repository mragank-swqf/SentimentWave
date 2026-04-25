import requests


res = requests.post("http://localhost:8000/analyze/6")
print(res.json())