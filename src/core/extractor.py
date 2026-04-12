"""
Product data extraction from page elements.
"""
from .cleaner import clean_product_name, clean_price, clean_text


class ProductExtractor:
    """Extract product information from page elements."""
    
    @staticmethod
    def extract_aldi(item):
        """
        Extract product data from ALDI product tile.
        
        Args:
            item: Playwright element selector for product tile
            
        Returns:
            dict: Product data with keys: brand, name, price, quantity, link
        """
        product = {}
        
        try:
            # brand
            brand_el = item.query_selector('.product-tile__content__upper__brand-name')
            product['brand'] = clean_text(brand_el.inner_text()) if brand_el else None
            
            # name
            name_el = item.query_selector('.product-tile__content__upper__product-name')
            raw_name = name_el.inner_text().strip() if name_el else None
            product['name'] = clean_product_name(raw_name)
            
            # price
            price_el = item.query_selector('.tag__label--price')
            price_text = price_el.inner_text().strip() if price_el else None
            product['price'] = clean_price(price_text)
            
            # quantity/size
            quantity_el = item.query_selector('.tag__marker--salesunit')
            product['quantity'] = clean_text(quantity_el.inner_text()) if quantity_el else None
            
            # link
            link_el = item.query_selector('a.product-tile__action')
            if link_el:
                href = link_el.get_attribute("href")
                product['link'] = "https://www.aldi.nl" + href if href else None
            else:
                product['link'] = None
                
            product['store'] = 'ALDI'
            
        except Exception as e:
            raise Exception(f"Error extracting ALDI product: {e}")
        
        return product
    
    @staticmethod
    def extract_jumbo(item):
        """
        Extract product data from Jumbo product container.
        
        Args:
            item: Playwright element selector for product container
            
        Returns:
            dict: Product data
        """
        product = {}
        
        try:
            name_el = item.query_selector("h3")
            whole_el = item.query_selector(".whole")
            frac_el = item.query_selector(".fractional")
            link_el = item.query_selector("a[href]")
            img_el = item.query_selector("img")
            
            if not name_el or not whole_el or not frac_el:
                return None
            
            product['name'] = clean_product_name(name_el.inner_text())
            
            try:
                price = float(f"{whole_el.inner_text().strip()}.{frac_el.inner_text().strip()}")
                product['price'] = price
            except ValueError:
                product['price'] = None
            
            if link_el:
                href = link_el.get_attribute("href")
                product['link'] = "https://www.jumbo.com" + href if href else None
            else:
                product['link'] = None
            
            product['image_url'] = img_el.get_attribute("src") if img_el else None
            product['store'] = 'Jumbo'
            product['category'] = 'dairy_eggs'
            
        except Exception as e:
            raise Exception(f"Error extracting Jumbo product: {e}")
        
        return product
    
    @staticmethod
    def extract_vomar(item):
        """
        Extract product data from Vomar product element.
        
        Args:
            item: Playwright element selector for product
            
        Returns:
            dict: Product data
        """
        product = {}
        
        try:
            name_el = item.query_selector(".description")
            whole_el = item.query_selector(".large")
            frac_el = item.query_selector(".small")
            link_el = item.query_selector("a")
            img_el = item.query_selector("img")
            
            if not name_el or not whole_el or not frac_el:
                return None
            
            product['name'] = clean_product_name(name_el.inner_text())
            
            try:
                price = float(
                    f"{whole_el.inner_text().replace('.', '').strip()}."
                    f"{frac_el.inner_text().strip()}"
                )
                product['price'] = price
            except ValueError:
                product['price'] = None
            
            if link_el:
                href = link_el.get_attribute("href")
                product['link'] = "https://www.vomar.nl" + href if href else None
            else:
                product['link'] = None
            
            product['image_url'] = img_el.get_attribute("src") if img_el else None
            product['store'] = 'Vomar'
            product['category'] = 'dairy_eggs'
            
        except Exception as e:
            raise Exception(f"Error extracting Vomar product: {e}")
        
        return product
