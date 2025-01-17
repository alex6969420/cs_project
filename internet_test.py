import requests

try:
    response = requests.get("https://www.google.com")
    print("Connected to the internet!")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")