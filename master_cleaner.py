import json
import re
import os
from pathlib import Path
from datetime import datetime

def clean_product_name(text):
    """Clean and normalize product name."""
    if not text:
        return ""
    
    text = text.lower()
    
    # Normalize units
    unit_mappings = {
        r'\blitre\b': 'l',
        r'\bliter\b': 'l',
        r'\bgramme\b': 'g',
        r'\bgram\b': 'g',
        r'\bkilogram\b': 'kg',
        r'\bkg\b': 'kg',
        r'\bmillilitre\b': 'ml',
        r'\bmilliliter\b': 'ml',
        r'\bml\b': 'ml',
        r'\bstuks\b': 'pcs',
        r'\bpieces\b': 'pcs',
    }
    
    for old, new in unit_mappings.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    
    # Remove special characters
    text = re.sub(r'[^\w\s\-/]', '', text, flags=re.UNICODE)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def clean_price(text):
    """Clean and normalize price strings."""
    if not text:
        return None
    
    if isinstance(text, (int, float)):
        return float(text)
    
    text = str(text)
    text = re.sub(r'[^\d,.]', '', text).strip()
    
    if ',' in text and '.' in text:
        if text.rfind(',') > text.rfind('.'):
            text = text.replace('.', '').replace(',', '.')
        else:
            text = text.replace(',', '')
    elif ',' in text:
        text = text.replace(',', '.')
    
    try:
        return float(text)
    except ValueError:
        return None


def extract_quantity(name, size_field=None):
    """Extract quantity from name or size field."""
    quantity = None
    
    # Check size field first
    if size_field:
        quantity = clean_product_name(str(size_field))
    
    # Extract from name (e.g., "1l", "500g", "12 pcs")
    if not quantity and name:
        match = re.search(r'(\d+\s*(?:ml|l|g|kg|pcs|stuks))', name.lower())
        if match:
            quantity = match.group(1).replace(' ', '')
    
    return quantity if quantity else None


def normalize_product(product, store_name):
    """
    Normalize a product to standard format regardless of source store.
    
    Standard format:
    {
        "store": "ALDI",
        "brand": "Campina",
        "name": "milk 1l",
        "price": 1.29,
        "quantity": "1l",
        "link": "https://...",
        "category": "dairy",
        "image_url": "https://...",
        "cleaned_at": "2026-04-12T16:00:00"
    }
    """
    
    # Extract fields based on store type
    if store_name.lower() == 'aldi':
        return {
            'store': 'ALDI',
            'brand': product.get('brand', '').strip(),
            'name': clean_product_name(product.get('name', '')),
            'price': clean_price(product.get('price', '')),
            'quantity': extract_quantity(product.get('name', ''), product.get('size', '')),
            'link': product.get('link', ''),
            'category': 'dairy_eggs',
            'image_url': product.get('image', ''),
            'cleaned_at': datetime.now().isoformat(),
        }
    
    elif store_name.lower() == 'jumbo':
        return {
            'store': 'Jumbo',
            'brand': '',  # Jumbo doesn't provide brand
            'name': clean_product_name(product.get('name', '')),
            'price': clean_price(product.get('price', '')),
            'quantity': extract_quantity(product.get('name', '')),
            'link': product.get('product_url', ''),
            'category': product.get('category', 'dairy_eggs'),
            'image_url': product.get('image_url', ''),
            'cleaned_at': datetime.now().isoformat(),
        }
    
    elif store_name.lower() == 'vomar':
        return {
            'store': 'Vomar',
            'brand': '',  # Vomar doesn't provide brand
            'name': clean_product_name(product.get('name', '')),
            'price': clean_price(product.get('price', '')),
            'quantity': extract_quantity(product.get('name', '')),
            'link': product.get('product_url', '') or product.get('link', ''),
            'category': product.get('category', 'dairy_eggs'),
            'image_url': product.get('image_url', '') or product.get('image', ''),
            'cleaned_at': datetime.now().isoformat(),
        }
    
    elif store_name.lower() == 'ah' or store_name.lower() == 'albert heijn':
        return {
            'store': 'Albert Heijn',
            'brand': '',
            'name': clean_product_name(product.get('name', '')),
            'price': clean_price(product.get('price', '')),
            'quantity': extract_quantity(product.get('name', '')),
            'link': product.get('link', ''),
            'category': 'dairy_eggs',
            'image_url': product.get('image', '') or product.get('image_url', ''),
            'cleaned_at': datetime.now().isoformat(),
        }
    
    return None


def clean_store_json(input_path, store_name):
    """Clean a single store's JSON file."""
    print(f"Processing {store_name}...")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print(f"  Error reading: {e}")
        return None
    
    cleaned = []
    for product in products:
        normalized = normalize_product(product, store_name)
        if normalized:
            cleaned.append(normalized)
    
    print(f"  Cleaned {len(cleaned)}/{len(products)} products")
    return cleaned


def main():
    """Clean all store JSONs and create unified output."""
    print("=" * 60)
    print("🧹 UNIFIED PRODUCT CLEANER")
    print("=" * 60)
    
    # Define store files
    stores = [
        ('output/aldi_2026-04-12_16-04.json', 'ALDI'),
        ('output/jumbo_dairy_2026-04-12_13-41.json', 'Jumbo'),
        ('output/vomar_dairy_2026-04-12_14-20.json', 'Vomar'),
    ]
    
    all_cleaned = []
    
    # Clean each store
    for file_path, store_name in stores:
        if not Path(file_path).exists():
            print(f"⚠️  File not found: {file_path}")
            continue
        
        cleaned_products = clean_store_json(file_path, store_name)
        if cleaned_products:
            all_cleaned.extend(cleaned_products)
    
    # Save unified output
    os.makedirs('output/processed', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Timestamped file
    output_file = f'output/processed/all_stores_cleaned_{timestamp}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_cleaned, f, indent=2, ensure_ascii=False)
    
    # Latest file
    with open('output/processed/all_stores_cleaned_latest.json', 'w', encoding='utf-8') as f:
        json.dump(all_cleaned, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"✅ COMPLETE")
    print("=" * 60)
    print(f"Total products cleaned: {len(all_cleaned)}")
    print(f"Saved to: {output_file}")
    print(f"Latest: output/processed/all_stores_cleaned_latest.json")
    print("=" * 60)


if __name__ == "__main__":
    main()
