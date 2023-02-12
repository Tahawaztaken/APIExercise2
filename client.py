import requests, json

def fetch_api():
    response = requests.get("http://127.0.0.1:5000/api/measurements")
    return response.json()
    
def fetch_last100():
    response = requests.get("http://127.0.0.1:5000/api/top100")
    abc = response.json()
    return abc

def fetch_stats(startTime, endTime):
    response = requests.get(f"http://127.0.0.1:5000/api/stats?startDate='{startTime}'&endDate='{endTime}'")
    return response.json()

print(fetch_stats('00:30:00', '00:35:00'))