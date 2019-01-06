import requests

url = "http://www.tel.uva.es"

response = requests.get(url)

print response.status_code
print response.text