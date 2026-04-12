from playwright.sync_api import sync_playwright
import json
import time
from datetime import datetime


BASE_URL = "https://www.ah.nl/producten/1730/zuivel-eieren?page={}"


def scrape_page(page, page_num):
    url = BASE_URL.format(page_num)
    print(f"\nScraping page {page_num}...")

    page.goto(url, timeout=60000)

    # 👇 simulate real user
    page.wait_for_timeout(5000)

    # scroll to trigger lazy load
    page.mouse.wheel(0, 5000)
    page.wait_for_timeout(3000)

    items = page.query_selector_all('[data-testid="product-card-vertical-container"]')

    print(f"Found {len(items)} products")

    results = []

    for item in items:
        try:
            name = item.query_selector("p").inner_text()

            price_whole = item.query_selector('.current-price_root__8Ka3V p')
            price_decimal = item.query_selector('.current-price_cents__VCUS4')

            price = None
            if price_whole and price_decimal:
                price = f"{price_whole.inner_text()}.{price_decimal.inner_text()}"

            results.append({
                "name": name,
                "price": price
            })

        except Exception as e:
            print("Error:", e)

    return results


def run():
    all_products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()

        for i in range(1, 20):
            data = scrape_page(page, i)

            if len(data) == 0:
                print("❌ Blocked or end reached")
                break

            all_products.extend(data)

        browser.close()

    print(f"\n✅ Total products: {len(all_products)}")


if __name__ == "__main__":
    run()
