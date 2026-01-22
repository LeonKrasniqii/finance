import requests
from bs4 import BeautifulSoup
from typing import Dict


def fetch_exchange_rates() -> Dict[str, float]:
    """
    Fetches current exchange rates from USD to other currencies.
    Returns a dictionary mapping currency name to exchange rate (float).
    """
    url = "https://www.x-rates.com/table/?from=USD&amount=1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch exchange rates: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    rates = {}
    table = soup.find("table")
    if not table:
        raise RuntimeError("Exchange rates table not found on page")

    rows = table.find_all("tr")[1:]  # Skip header
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            currency = cols[0].text.strip()
            try:
                rate = float(cols[1].text.strip())
                rates[currency] = rate
            except ValueError:
                # Skip invalid entries
                continue

    return rates
