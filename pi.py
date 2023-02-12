import time, requests, random


def fetch_api():
    random_number = random.randint(0, 100)
    random_Ip = f"{random.randint(127, 130)}.0.0.{random.randint(0, 10)}"
    response = requests.post(f"http://127.0.0.1:5000/api/measurements?address='{random_Ip}'&value={random_number}")
    print(response)

while True:
    fetch_api()
    time.sleep(1) 