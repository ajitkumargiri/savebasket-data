import json
from .cleaner import clean_product_name, clean_price
import re

def clean_aldi_json(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    cleaned = []
    for p in products:
        cleaned_product = {
            'store': p.get('store', 'ALDI'),
            'brand': p.get('brand', ''),
            'name': clean_product_name(p.get('name', '')),
            'price': clean_price(p.get('price', '')),
            'quantity': clean_product_name(p.get('size', '')),
            'link': p.get('link', ''),
            'image': p.get('image', ''),
            # Add more fields as needed for DB
        }
        cleaned.append(cleaned_product)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    return cleaned

if __name__ == "__main__":
    # Example usage
    clean_aldi_json(
        '../../output/aldi_2026-04-12_16-04.json',
        '../../output/aldi_cleaned.json'
    )
