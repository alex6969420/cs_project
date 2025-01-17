import requests

API_KEY = '27420f6a219b93aada8ff0d82588b295'
APP_ID = 'd2234145'
barcode = '0687456211022'  # Replace with your test barcode
API_URL = f'https://api.nutritionix.com/v1_1/item?upc={barcode}&appId={APP_ID}&appKey={API_KEY}'

try:
    response = requests.get(API_URL)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response Data:", response.json())
    else:
        print("API Error:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Connection Error: {e}")
