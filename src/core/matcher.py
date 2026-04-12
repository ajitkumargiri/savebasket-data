"""
Product matching and deduplication utilities.
"""
from difflib import SequenceMatcher


class ProductMatcher:
    """Match and deduplicate products across stores."""
    
    @staticmethod
    def similarity_ratio(a, b):
        """
        Calculate similarity ratio between two strings (0-1).
        
        Args:
            a: First string
            b: Second string
            
        Returns:
            float: Similarity ratio between 0 and 1
        """
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    @staticmethod
    def is_same_product(product1, product2, name_threshold=0.85, price_threshold=0.1):
        """
        Check if two products are the same across different stores.
        
        Args:
            product1: First product dict
            product2: Second product dict
            name_threshold: Minimum name similarity (0-1)
            price_threshold: Maximum price difference ratio (0-1)
            
        Returns:
            bool: True if products appear to be the same
        """
        if not product1.get('name') or not product2.get('name'):
            return False
        
        # Check name similarity
        name_sim = ProductMatcher.similarity_ratio(
            product1['name'],
            product2['name']
        )
        
        if name_sim < name_threshold:
            return False
        
        # Check price similarity if both have prices
        price1 = product1.get('price')
        price2 = product2.get('price')
        
        if price1 and price2:
            price_diff = abs(price1 - price2) / max(price1, price2)
            if price_diff > price_threshold:
                return False
        
        return True
    
    @staticmethod
    def find_duplicates(products, name_threshold=0.85):
        """
        Find duplicate products in a list.
        
        Args:
            products: List of product dicts
            name_threshold: Minimum name similarity
            
        Returns:
            List of lists, each containing indices of duplicate products
        """
        duplicates = []
        seen = set()
        
        for i in range(len(products)):
            if i in seen:
                continue
            
            group = [i]
            for j in range(i + 1, len(products)):
                if j in seen:
                    continue
                
                if ProductMatcher.is_same_product(
                    products[i],
                    products[j],
                    name_threshold=name_threshold
                ):
                    group.append(j)
                    seen.add(j)
            
            if len(group) > 1:
                duplicates.append(group)
                seen.add(i)
        
        return duplicates
    
    @staticmethod
    def deduplicate(products, keep_first=True, name_threshold=0.85):
        """
        Remove duplicate products from list.
        
        Args:
            products: List of product dicts
            keep_first: If True, keep first occurrence; otherwise keep best quality
            name_threshold: Minimum name similarity for deduplication
            
        Returns:
            List of deduplicated products
        """
        duplicate_groups = ProductMatcher.find_duplicates(products, name_threshold)
        
        indices_to_remove = set()
        for group in duplicate_groups:
            # Remove all but the first (or best quality)
            if keep_first:
                indices_to_remove.update(group[1:])
            else:
                # Keep the one with most data
                best_idx = max(group, key=lambda i: sum(1 for v in products[i].values() if v))
                indices_to_remove.update(i for i in group if i != best_idx)
        
        return [p for i, p in enumerate(products) if i not in indices_to_remove]
