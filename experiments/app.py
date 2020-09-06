import os
import requests
from slugify import slugify
from bs4 import BeautifulSoup


baseURI = "https://laravel.com"

version = "6.x"

linksMarkup = {
    'tag': 'div',
    'class': 'docs_sidebar'
}

docsMarkup = {
    'tag': 'section',
    'class': 'docs_main'
}

if not os.path.exists(f"builds/{version}"):
    os.makedirs(f"builds/{version}")

response = requests.get(f"{baseURI}/docs/{version}")

if not response.status_code == 200:

    print("NOT OKAY")
    quit()

soup = BeautifulSoup(response.content, 'html.parser')

linksSrc = soup.find_all(linksMarkup['tag'], {
    'class': linksMarkup['class']
}, limit=1)

links = []

for link in linksSrc[0].findAll('a'):

    links.append(f"{baseURI}{link.get('href')}")

for link in links:

    if "github.com" in link:

        continue

    response = requests.get(link)

    if not response.status_code == 200:

        print("Unable to fetch link: ", link)

        continue

    else:

        print("Building link: ", link)

    soup = BeautifulSoup(response.content, 'html.parser')

    documentation = soup.select_one(f".{docsMarkup['class']}")

    if str(documentation) == None:

        continue

    path = f"builds/{version}/{link.split('/')[-1]}.html"

    with open(path, 'w') as document:

        try:
            document.write(str(documentation))
        except UnicodeEncodeError:
            print('Unable to build link: ', link)
