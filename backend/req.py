import requests
res = requests.post("http://localhost:8000/analyze/3")
print(res.json())