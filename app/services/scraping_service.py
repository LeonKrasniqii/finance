# app/services/scraping_service.py

import requests
from bs4 import BeautifulSoup


def fetch_exchange_rates():
    url = "https://www.x-rates.com/table/?from=USD&amount=1"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    rates = {}
    table = soup.find("table")
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        rates[cols[0].text.strip()] = cols[1].text.strip()

    return rates
