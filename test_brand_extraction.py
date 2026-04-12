#!/usr/bin/env python3
"""Test brand extraction from product names."""

def extract_brand_from_name(product_name):
    """Extract brand from product name."""
    if not product_name:
        return ""
    
    brands = [
        'campina', 'melkunie', 'friesche', 'anchor', 'milsani', 'optimel',
        'yoplait', 'danone', 'arla', 'emmi', 'lactalis', 'vaalia', 'muller',
        'activia', 'maestrani', 'caerphilly', 'président', 'saint-moret',
        'kiri', 'milram', 'sura', 'zott', 'flora', 'becel', 'rama', 'domo'
    ]
    
    name_lower = product_name.lower()
    
    for brand in brands:
        if name_lower.startswith(brand):
            return brand.capitalize()
    
    words = product_name.split()
    if words and words[0][0].isupper() and not words[0].isdigit():
        return words[0]
    
    return ""


# Test with sample Jumbo product names
test_products = [
    "Campina Vla Limited Edition 1L",
    "Melkunie Boter 200g",
    "Friesche Melk Halfvolle 1L",
    "Activia Yoghurt Naturel 500g",
    "Danone Kwark Magere",
    "Store Brand Milk 1L",
    "1 Liter Melk",
    "Yoplait Nature 200g"
]

print("Brand Extraction Tests")
print("=" * 60)
for product in test_products:
    brand = extract_brand_from_name(product)
    print(f"Product: {product:40} | Brand: {brand}")
print("=" * 60)
