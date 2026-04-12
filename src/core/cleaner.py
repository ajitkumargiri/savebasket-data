"""
Text cleaning and normalization utilities for product data.
"""
import re


def clean_product_name(text):
    """
    Clean and normalize product name:
    - Convert to lowercase
    - Normalize common units
    - Remove special characters except spaces and numbers
    
    Args:
        text: Product name string to clean
        
    Returns:
        Cleaned product name string
    """
    if not text:
        return text
    
    # Convert to lowercase
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
    }
    
    for old, new in unit_mappings.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    
    # Remove special characters (keep letters, numbers, spaces, hyphens, and slashes)
    text = re.sub(r'[^\w\s\-/]', '', text, flags=re.UNICODE)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def clean_price(text):
    """
    Clean and normalize price strings.
    
    Args:
        text: Price string (e.g., "€ 2,50" or "2.50")
        
    Returns:
        Float price value or None if invalid
    """
    if not text:
        return None
    
    # Remove currency symbols and spaces
    text = re.sub(r'[^\d,.]', '', text).strip()
    
    # Handle both comma and period as decimal separator
    if ',' in text and '.' in text:
        # If both exist, use the last one as decimal
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


def clean_text(text):
    """
    Basic text cleaning without unit/price normalization.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return text
    
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text
