import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_page(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def scrape_prices(
    url: str,
    css_selector: str
) -> List[float]:
    html = scrape_page(url)
    soup = BeautifulSoup(html, "html.parser")

    prices = []
    elements = soup.select(css_selector)

    for el in elements:
        text = el.get_text(strip=True)
        clean = text.replace("$", "").replace(",", "")

        try:
            prices.append(float(clean))
        except ValueError:
            continue

    return prices

def scrape_categories(
    url: str,
    css_selector: str
) -> List[str]:
    html = scrape_page(url)
    soup = BeautifulSoup(html, "html.parser")

    return [
        el.get_text(strip=True)
        for el in soup.select(css_selector)
    ]

def scrape_exchange_rates(api_url: str) -> Dict[str, float]:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data.get("rates", {})
