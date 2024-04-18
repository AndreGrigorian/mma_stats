import requests
from bs4 import BeautifulSoup


# Replace with the actual URL
def find_fighter(name: str):
    fighter_name = name.replace(" ", "%20").lower()
    url = f'https://www.espn.com/search/_/q/{fighter_name}'
    response = requests.get(url)
