import requests

scr = "https://dog.ceo/api/breeds/image/random"
url = requests.get(scr)

print (url.text)