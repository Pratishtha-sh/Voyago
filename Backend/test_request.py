import requests
from datetime import date, timedelta

url = "http://127.0.0.1:8002/travel/analyze"

payload = {
    "source_city": "New York",
    "destination_city": "London",
    "travel_date": (date.today() + timedelta(days=30)).isoformat(),
    "duration_days": 5
}

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    import json
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
