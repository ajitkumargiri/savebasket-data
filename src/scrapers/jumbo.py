"""Jumbo scraper using Playwright."""
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

from ..core.extractor import ProductExtractor
from ..utils.logger import Logger


logger = Logger(__name__)

BASE_URL = "https://www.jumbo.com/producten/zuivel,-eieren,-boter/?offSet={}"
STEP = 24  # products per page


def scrape_page(page, offset):
    """Scrape a single offset/page from Jumbo."""
    url = BASE_URL.format(offset)
    logger.debug(f"Scraping offset {offset}...")

    try:
        page.goto(url, timeout=60000)
    except:
        logger.warning("Retrying page load...")
        page.goto(url, timeout=60000)

    page.wait_for_load_state("domcontentloaded")

    # Wait for actual products
    try:
        page.wait_for_selector("article.product-container", timeout=60000)
    except:
        logger.debug("No products found → likely end")
        return []

    page.wait_for_timeout(2000)

    items = page.query_selector_all("article.product-container")
    logger.debug(f"Found {len(items)} items")

    data = []

    for item in items:
        try:
            product = ProductExtractor.extract_jumbo(item)
            if product:
                data.append(product)
        except Exception as e:
            logger.debug(f"Error parsing product: {e}")
            continue

    return data


def run():
    """Main scraper runner."""
    all_data = []
    offset = 0

    logger.start_scraping("Jumbo")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        while True:
            data = scrape_page(page, offset)

            if not data:
                logger.info("No more products → stopping")
                break

            all_data.extend(data)
            logger.progress(offset // STEP + 1, -1, f"({len(all_data)} products so far)")

            offset += STEP
            time.sleep(2)  # polite scraping

        browser.close()

    # Save files
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"output/raw/jumbo_dairy_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    with open("output/raw/jumbo_dairy_latest.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    logger.end_scraping("Jumbo", len(all_data))
    logger.info(f"📁 Saved: {filename}")
    logger.info("📌 Updated latest file")
    
    return all_data


if __name__ == "__main__":
    run()
