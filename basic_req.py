import requests

url = "https://xn--42cah7d0cxcvbbb9x.com/"

response = requests.get(url)

html = response.text
print(html)
