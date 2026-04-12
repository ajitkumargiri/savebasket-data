"""
Main scraping pipeline to run all store scrapers.
"""
import json
from datetime import datetime
from pathlib import Path

from ..scrapers import aldi, jumbo, vomar, ah
from ..core.matcher import ProductMatcher
from ..utils.logger import Logger


logger = Logger(__name__)


def run_all_scrapers():
    """Run all scrapers and collect data from all stores."""
    logger.info("=" * 60)
    logger.info("🛒 STARTING FULL SCRAPING PIPELINE")
    logger.info("=" * 60)
    
    all_products = []
    results = {}
    
    # Run each scraper
    scrapers = [
        ("ALDI", aldi.run),
        ("Jumbo", jumbo.run),
        ("Vomar", vomar.run),
        ("Albert Heijn", ah.run),
    ]
    
    for name, scraper_func in scrapers:
        try:
            logger.info(f"\n▶️  Running {name} scraper...")
            products = scraper_func()
            results[name] = len(products)
            all_products.extend(products)
            logger.info(f"✅ {name}: {len(products)} products")
        except Exception as e:
            logger.error(f"❌ {name} scraper failed: {e}")
            results[name] = 0
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 SCRAPING SUMMARY")
    logger.info("=" * 60)
    for name, count in results.items():
        logger.info(f"{name}: {count} products")
    logger.info(f"TOTAL: {len(all_products)} products")
    logger.info("=" * 60)
    
    # Save combined raw data
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    combined_file = f"output/raw/all_stores_{timestamp}.json"
    
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)
    
    with open("output/raw/all_stores_latest.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n📁 Combined data saved: {combined_file}")
    logger.info("📌 Updated: output/raw/all_stores_latest.json")
    
    return all_products


def process_and_deduplicate(threshold=0.85):
    """Process products and remove duplicates."""
    logger.info("\n" + "=" * 60)
    logger.info("🔄 PROCESSING AND DEDUPLICATING")
    logger.info("=" * 60)
    
    # Load latest combined data
    latest_file = "output/raw/all_stores_latest.json"
    
    if not Path(latest_file).exists():
        logger.warning(f"Input file not found: {latest_file}")
        return []
    
    with open(latest_file, "r", encoding="utf-8") as f:
        products = json.load(f)
    
    logger.info(f"Loaded {len(products)} products from raw data")
    
    # Find and remove duplicates
    duplicates = ProductMatcher.find_duplicates(products, name_threshold=threshold)
    logger.info(f"Found {len(duplicates)} duplicate groups")
    
    unique_products = ProductMatcher.deduplicate(products, name_threshold=threshold)
    logger.info(f"After deduplication: {len(unique_products)} unique products")
    
    # Save processed data
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    processed_file = f"output/processed/all_stores_processed_{timestamp}.json"
    
    with open(processed_file, "w", encoding="utf-8") as f:
        json.dump(unique_products, f, indent=2, ensure_ascii=False)
    
    with open("output/processed/all_stores_processed_latest.json", "w", encoding="utf-8") as f:
        json.dump(unique_products, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n📁 Processed data saved: {processed_file}")
    logger.info("📌 Updated: output/processed/all_stores_processed_latest.json")
    
    return unique_products


def main():
    """Main entry point - run full pipeline."""
    # Run all scrapers
    all_products = run_all_scrapers()
    
    # Process and deduplicate
    processed_products = process_and_deduplicate(threshold=0.85)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ PIPELINE COMPLETE!")
    logger.info("=" * 60)
    logger.info(f"Raw products: {len(all_products)}")
    logger.info(f"Processed products: {len(processed_products)}")
    logger.info("Check output/raw/ and output/processed/ for results")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
