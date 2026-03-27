import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

URL = "https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22"

def scrape():
    res = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    fruits = []
    # Tìm bảng stock trong trang
    tables = soup.find_all("table", class_="wikitable")
    for table in tables:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                name = cols[0].get_text(strip=True)
                price = cols[1].get_text(strip=True).replace(",", "").replace(" Beli", "")
                if name:
                    fruits.append({
                        "name": name,
                        "price": int(price) if price.isdigit() else 0
                    })

    fruits.sort(key=lambda x: x["price"], reverse=True)

    out = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "stock": fruits
    }

    with open("data/stock.json", "w") as f:
        json.dump(out, f, indent=2)

    print(f"Done: {len(fruits)} fruits")

scrape()
