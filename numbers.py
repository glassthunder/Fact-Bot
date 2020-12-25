import requests

while True:
    link = "http://numbersapi.com/random/trivia"
    request = requests.get(link)
    print(request.text)
    break