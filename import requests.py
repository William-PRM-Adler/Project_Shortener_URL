import requests

response = requests.get("http://127.0.0.1:8000/list_of_urls")
print("Response Status:", response.status_code)
print("Response Data:", response.text)