import requests
from utils.utils import API_URL

url = f"{API_URL}/students"
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
