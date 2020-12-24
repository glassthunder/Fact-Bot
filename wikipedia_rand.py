import requests
from bs4 import BeautifulSoup
import webbrowser

while True:
    link = "https://en.wikipedia.org/wiki/Special:Random"
    request = requests.get(link)
    scraper = BeautifulSoup(request.content, "html.parser")
    title = scraper.find(class_= "firstHeading").text
    print("\nDo you want to read about " + title + "?")
    answer = raw_input("Type Y or N: ")

    if (answer.upper() == "Y"):
        article = 'https://en.wikipedia.org/wiki/%s' %title
        webbrowser.open(article)
        break
    elif (answer.upper() == "N"):
        print("Generating another article...")
        continue
    else:
        print("Invalid Answer. Rerun the program and try again.")
        break
