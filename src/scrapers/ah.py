"""Albert Heijn (AH) scraper using Playwright."""
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

from ..core.cleaner import clean_product_name, clean_price
from ..utils.logger import Logger


logger = Logger(__name__)

BASE_URL = "https://www.ah.nl/producten/1730/zuivel-eieren?page={}"


def scrape_page(page, page_num):
    """Scrape a single page from Albert Heijn."""
    url = BASE_URL.format(page_num)
    logger.debug(f"Scraping page {page_num}...")

    page.goto(url, timeout=60000)

    # Simulate real user behavior
    page.wait_for_timeout(5000)

    # Scroll to trigger lazy load
    page.mouse.wheel(0, 5000)
    page.wait_for_timeout(3000)

    items = page.query_selector_all('[data-testid="product-card-vertical-container"]')
    logger.debug(f"Found {len(items)} products")

    results = []

    for item in items:
        try:
            # Extract name
            name_el = item.query_selector("p")
            name = name_el.inner_text() if name_el else None
            name = clean_product_name(name)

            # Extract price
            price_whole = item.query_selector('.current-price_root__8Ka3V p')
            price_decimal = item.query_selector('.current-price_cents__VCUS4')

            price = None
            if price_whole and price_decimal:
                price_str = f"{price_whole.inner_text()}.{price_decimal.inner_text()}"
                price = clean_price(price_str)

            if name:  # Only add if we have a name
                results.append({
                    "store": "Albert Heijn",
                    "name": name,
                    "price": price
                })

        except Exception as e:
            logger.debug(f"Error parsing product: {e}")

    return results


def run():
    """Main scraper runner."""
    all_products = []

    logger.start_scraping("Albert Heijn")

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
                logger.warning("Blocked or end reached")
                break

            all_products.extend(data)
            logger.progress(i, 20, f"({len(all_products)} products so far)")

        browser.close()

    # Save files
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"output/raw/ah_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)

    with open("output/raw/ah_latest.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)

    logger.end_scraping("Albert Heijn", len(all_products))
    logger.info(f"📁 Saved: {filename}")
    logger.info("📌 Updated latest file")
    
    return all_products


if __name__ == "__main__":
    run()
