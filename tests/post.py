import requests
from utils.utils import API_URL

url = f"http://192.168.1.162:8000/api/students"

student_data = {
                "rfid": 12345678,
                "alias": "Al",
                "first_name": "test",
                "last_name": "test last name",
                "middle_name": "NA",
                "email": "admin@test.com",
                "password": "1234567890"
            }

response = requests.post(url, data=student_data)
print(response)
