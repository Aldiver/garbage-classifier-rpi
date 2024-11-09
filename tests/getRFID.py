import requests
from utils.utils import API_URL

url = f"{API_URL}/rfid/0007424052"
response = requests.get(url)
print(response.text)
