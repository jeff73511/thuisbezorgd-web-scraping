import requests
from bs4 import BeautifulSoup
import json

url = "https://www.thuisbezorgd.nl/en/order-takeaway-amsterdam-1066"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
cuisines = soup.findAll("a", {"data-type": "Cuisine"})[1:]

cuisine_styles = [cuisine.text.strip() for cuisine in cuisines]
cuisine_dic = dict(zip(cuisine_styles, list(range(2, 51))))

with open("cuisine_dic.json", "w") as file:
    file.write(json.dumps(cuisine_dic))
