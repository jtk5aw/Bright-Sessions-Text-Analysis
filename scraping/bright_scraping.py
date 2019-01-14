# Bright Sessions Web Scraping Code
import json
import time
import requests
import unicodedata
from bs4 import BeautifulSoup

# Base URL for all episodes
URL = "http://thebrightsessions.com/episode-"

# Gets the lines from the current webpage
def getLines(c):
    # Puts the webpage into a BeautifulSoup object to parse it
    soup = BeautifulSoup(c, features="lxml")
    # Found that all the text is contained within this block and each line is in an individual <p> block
    content = soup.find("div", {"id": "content", "class": "main-content"})
    paragraphs = content.findAll("p")
    # Creates a list of the lines for this episode
    lines = []
    for line in paragraphs:
      lines.append(unicodedata.normalize("NFKD", line.get_text()))
    return lines

# Waits until the status code is 200 and then returns the requests content
def getRequestContent(eps):
    result = requests.get(URL+eps)
    while result.status_code != 200:
        # Waits if the status code returned wasn't succesful and then tries again
        time.sleep(10)
        result = requests.get(URL+eps)
    print("Sucessfully recieved " + eps)
    return result.content

scripts = {}
# Episode 17 was split into two episodes and needs to be handled seperately
episodes = [i for i in range(1,57) if i != 17]
for i in episodes:
    # Gets the current website and prints the status code of the result
    content = getRequestContent(str(i))
    # Creates the lines
    scripts[i] = getLines(content)

# Gets the script for the two 17th episodes and combines them
eps17a = getRequestContent("17a")
eps17b = getRequestContent("17b")
scripts[17] = getLines(eps17a) + getLines(eps17b)

with open("../data/bright_scripts.json", "w") as outfile:
    json.dump(scripts, outfile, indent=4)
outfile.close()
