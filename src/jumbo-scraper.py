from playwright.sync_api import sync_playwright
import json
import os

URL = "https://www.jumbo.com/producten"

def scrape_jumbo():

    os.makedirs("output", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Opening Jumbo...")
        page.goto(URL, timeout=60000)

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        # scroll to load products
        for _ in range(10):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)

        items = page.query_selector_all("article.product-container")

        print(f"Found {len(items)} products")

        data = []

        for item in items[:50]:
            try:
                name_el = item.query_selector("h3")
                whole_el = item.query_selector(".whole")
                frac_el = item.query_selector(".fractional")

                if not name_el or not whole_el or not frac_el:
                    continue

                name = name_el.inner_text().strip()
                price = f"€{whole_el.inner_text().strip()}.{frac_el.inner_text().strip()}"

                data.append({
                    "store": "Jumbo",
                    "category": "all",
                    "name": name,
                    "price": price
                })

            except:
                continue

        browser.close()
        return data


def run():
    data = scrape_jumbo()

    with open("output/jumbo.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved {len(data)} products")


if __name__ == "__main__":
    run()
