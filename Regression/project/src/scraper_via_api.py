import requests
import pandas as pd
import time
import random
import json
from typing import List, Dict, Optional
from datetime import datetime
import os


class TokopediaScraper:
    """
    Production-ready Tokopedia Scraper using GraphQL API
    """
    
    def __init__(self):
        self.base_url = 'https://gql.tokopedia.com/graphql/SearchProductV5Query'
        self.session = requests.Session()
        self.setup_headers()
        
    def setup_headers(self):
        """Setup headers untuk request"""
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.tokopedia.com',
            'referer': 'https://www.tokopedia.com/',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-device': 'desktop-0.0',
            'x-source': 'tokopedia-lite',
            'x-tkpd-lite-service': 'zeus',
        }
        
        # PENTING: Cookies ini akan expire, perlu di-update berkala
        # Cara update: buka DevTools → copy cookies baru
        self.cookies = {
            '_UUID_NONLOGIN_': 'b66867e9aa8d3370535b7e4fd4b74830',
            '_gid': 'GA1.2.1680254013.1764831912',
            # Tambahkan cookies lain jika diperlukan
        }
    
    def build_graphql_payload(self, keyword: str, page: int = 1, rows: int = 60, 
                            category_id: str = None, min_price: int = None, max_price: int = None) -> List[Dict]:
        """
        Membuat GraphQL payload untuk search
        
        Args:
            keyword: Kata kunci pencarian (e.g., 'laptop')
            page: Nomor halaman (mulai dari 1)
            rows: Jumlah produk per halaman (max 60)
            category_id: Category ID untuk filter (e.g., '3639' untuk laptop)
            min_price: Harga minimum
            max_price: Harga maximum
        """
        start = (page - 1) * rows
        
        # Build params string dengan filter
        params = (
            f"device=desktop&enter_method=normal_search&"
            f"page={page}&q={keyword}&rows={rows}&start={start}&"
            f"ob=23&related=true&safe_search=false&scheme=https&"
            f"source=universe&st=product&topads_bucket=true"
        )
        
        # Tambahkan category filter jika ada
        if category_id:
            params += f"&sc={category_id}"
        
        # Tambahkan price filter jika ada
        if min_price:
            params += f"&pmin={min_price}"
        if max_price:
            params += f"&pmax={max_price}"
        
        payload = [{
            'operationName': 'SearchProductV5Query',
            'variables': {
                'params': params
            },
            'query': '''query SearchProductV5Query($params: String!) {
              searchProductV5(params: $params) {
                header {
                  totalData
                  responseCode
                  __typename
                }
                data {
                  products {
                    id
                    name
                    url
                    mediaURL {
                      image
                      __typename
                    }
                    shop {
                      id
                      name
                      city
                      tier
                      __typename
                    }
                    price {
                      text
                      number
                      original
                      discountPercentage
                      __typename
                    }
                    rating
                    labelGroups {
                      title
                      type
                      __typename
                    }
                    badge {
                      title
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                __typename
              }
            }'''
        }]
        
        return payload
    
    def search_products(self, keyword: str, page: int = 1, rows: int = 60,
                       category_id: str = None, min_price: int = None, max_price: int = None) -> Optional[Dict]:
        """
        Search produk di Tokopedia
        
        Returns:
            Dictionary berisi response data atau None jika gagal
        """
        payload = self.build_graphql_payload(keyword, page, rows, category_id, min_price, max_price)
        
        try:
            response = self.session.post(
                self.base_url,
                headers=self.headers,
                cookies=self.cookies,
                json=payload,
                timeout=15
            )
            
            print(f"[Page {page}] Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return data[0]  # GraphQL returns array with single item
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response: {response.text[:500]}")
            return None
    
    def parse_products(self, response_data: Dict) -> List[Dict]:
        """
        Parse response GraphQL menjadi list produk yang rapi
        """
        products = []
        
        try:
            product_list = response_data['data']['searchProductV5']['data']['products']
            
            for p in product_list:
                # Handle missing data with .get()
                shop = p.get('shop', {})
                price = p.get('price', {})
                media = p.get('mediaURL', {})
                badge = p.get('badge', {})
                
                # Extract label groups (e.g., "Terjual 100+", "Cashback")
                labels = [label.get('title', '') for label in p.get('labelGroups', [])]
                
                product = {
                    'id': p.get('id'),
                    'name': p.get('name'),
                    'price': price.get('number', 0),
                    'price_text': price.get('text', ''),
                    'original_price': price.get('original', 0),
                    'discount_percentage': price.get('discountPercentage', 0),
                    'rating': p.get('rating', 0),
                    'shop_name': shop.get('name', ''),
                    'shop_city': shop.get('city', ''),
                    'shop_tier': shop.get('tier', 0),
                    'badge': badge.get('title', ''),
                    'labels': '; '.join(labels),
                    'image_url': media.get('image', ''),
                    'product_url': p.get('url', ''),
                }
                
                products.append(product)
                
        except (KeyError, TypeError) as e:
            print(f"Parsing error: {e}")
            
        return products
    
    def scrape_multiple_pages(self, keyword: str, max_pages: int = 5, delay: tuple = (2, 4),
                             category_id: str = None, min_price: int = None, max_price: int = None,
                             filter_keywords: List[str] = None, exclude_keywords: List[str] = None) -> pd.DataFrame:
        """
        Scrape multiple pages dan return DataFrame
        
        Args:
            keyword: Kata kunci pencarian
            max_pages: Maksimal halaman yang di-scrape
            delay: Tuple (min, max) detik untuk random delay
            category_id: Filter by category ID
            min_price: Harga minimum
            max_price: Harga maksimum
            filter_keywords: Hanya ambil produk yang mengandung kata ini di nama (OR logic)
            exclude_keywords: Exclude produk yang mengandung kata ini di nama
        
        Returns:
            DataFrame berisi semua produk
        """
        all_products = []
        total_data = 0
        
        print(f"\n{'='*60}")
        print(f"🔍 Scraping Tokopedia: '{keyword}'")
        if category_id:
            print(f"📁 Category ID: {category_id}")
        # if min_price or max_price:
        #     print(f"💰 Price range: Rp {min_price:,} - Rp {max_price:,}")
        if filter_keywords:
            print(f"🔎 Filter keywords: {', '.join(filter_keywords)}")
        if exclude_keywords:
            print(f"🚫 Exclude keywords: {', '.join(exclude_keywords)}")
        print(f"{'='*60}\n")
        
        for page in range(1, max_pages + 1):
            print(f"📄 Scraping page {page}/{max_pages}...")
            
            # Request data
            response = self.search_products(keyword, page, category_id=category_id, 
                                          min_price=min_price, max_price=max_price)
            
            if response:
                # Get total data dari header (hanya di page 1)
                if page == 1:
                    try:
                        total_data = response['data']['searchProductV5']['header']['totalData']
                        print(f"📊 Total products available: {total_data:,}")
                    except:
                        pass
                
                # Parse products
                products = self.parse_products(response)
                
                # Apply keyword filters
                if filter_keywords or exclude_keywords:
                    products = self.filter_products(products, filter_keywords, exclude_keywords)
                
                if products:
                    all_products.extend(products)
                    print(f"✅ Found {len(products)} products (Total: {len(all_products)})")
                else:
                    print("⚠️  No products found on this page")
                    break
            else:
                print("❌ Request failed")
                break
            
            # Random delay untuk avoid rate limiting
            if page < max_pages:
                delay_time = random.uniform(delay[0], delay[1])
                print(f"⏳ Waiting {delay_time:.1f}s...\n")
                time.sleep(delay_time)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_products)
        
        print(f"\n{'='*60}")
        print(f"✨ Scraping Complete!")
        print(f"📊 Total products scraped: {len(df)}")
        print(f"{'='*60}\n")
        
        return df
    
    def filter_products(self, products: List[Dict], filter_keywords: List[str] = None, 
                       exclude_keywords: List[str] = None) -> List[Dict]:
        """
        Filter produk berdasarkan keywords di nama produk
        
        Args:
            products: List of product dictionaries
            filter_keywords: Hanya ambil produk yang mengandung kata ini (OR logic)
            exclude_keywords: Exclude produk yang mengandung kata ini
        """
        filtered = []
        
        for product in products:
            name_lower = product['name'].lower()
            
            # Check exclude keywords first
            if exclude_keywords:
                if any(keyword.lower() in name_lower for keyword in exclude_keywords):
                    continue
            
            # Check filter keywords (OR logic - salah satu match)
            if filter_keywords:
                if any(keyword.lower() in name_lower for keyword in filter_keywords):
                    filtered.append(product)
            else:
                filtered.append(product)
        
        return filtered
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None):
        """Save DataFrame ke CSV"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'tokopedia_laptops_{timestamp}.csv'
        
        # Create directory if not exists
        os.makedirs('../data/raw', exist_ok=True)
        filepath = f'../data/raw/{filename}'
        
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"💾 Saved to: {filepath}")
        
        return filepath
    
    def save_to_excel(self, df: pd.DataFrame, filename: str = None):
        """Save DataFrame ke Excel"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'tokopedia_laptops_{timestamp}.xlsx'
        
        os.makedirs('../data/raw', exist_ok=True)
        filepath = f'../data/raw/{filename}'
        
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"💾 Saved to: {filepath}")
        
        return filepath


def main():
    """
    Main function untuk menjalankan scraper
    """
    # Initialize scraper
    scraper = TokopediaScraper()
    
    # ============================================================
    # METODE 1: FILTER DENGAN KEYWORDS (PALING MUDAH)
    # ============================================================
    print("\n" + "="*60)
    print("METODE 1: Filter dengan Keywords")
    print("="*60)
    
    df_method1 = scraper.scrape_multiple_pages(
        keyword='laptop',
        max_pages=5,
        delay=(2, 4),
        min_price=3000000,  # Minimal 3 juta (laptop biasanya > 3 juta)
        max_price=50000000,  # Maksimal 50 juta
        exclude_keywords=[
            'tas', 'case', 'sleeve', 'cover', 'skin', 'cooler', 'cooling pad',
            'mouse', 'keyboard', 'charger', 'adaptor', 'kabel', 'cable',
            'stand', 'meja', 'table', 'dudukan', 'holder',
            'speaker', 'headset', 'webcam', 'mic', 'microphone',
            'ram', 'ssd', 'hardisk', 'hdd', 'flashdisk',
            'sticker', 'stiker', 'gantungan', 'dompet',
            'cleaning kit', 'pembersih', 'lap', 'screen protector',
            'adaptor', 'hub', 'converter', 'splitter', 'dock'
        ]
    )
    
    # ============================================================
    # METODE 2: LEBIH SPESIFIK DENGAN BRAND (RECOMMENDED)
    # ============================================================
    print("\n" + "="*60)
    print("METODE 2: Filter dengan Brand Names")
    print("="*60)
    
    df_method2 = scraper.scrape_multiple_pages(
        keyword='laptop',
        max_pages=5,
        delay=(2, 4),
        min_price=3000000,
        filter_keywords=[
            # Brand laptop terkenal
            'asus', 'lenovo', 'hp', 'dell', 'acer', 'msi', 
            'apple', 'macbook', 'thinkpad', 'ideapad', 'vivobook',
            'pavilion', 'inspiron', 'latitude', 'precision',
            'tuf', 'rog', 'predator', 'legion', 'nitro',
            'surface', 'razer', 'gigabyte', 'avita'
        ],
        exclude_keywords=[
            'tas', 'case', 'mouse', 'keyboard', 'charger', 
            'cooler', 'stand', 'ram', 'ssd'
        ]
    )
    
    # ============================================================
    # METODE 3: KEYWORD LEBIH SPESIFIK
    # ============================================================
    print("\n" + "="*60)
    print("METODE 3: Keyword Spesifik")
    print("="*60)
    
    # Coba berbagai keyword spesifik
    specific_keywords = [
        'laptop asus',
        'laptop gaming',
        'laptop core i5',
        'laptop ryzen',
        'notebook'
    ]
    
    # Pilih salah satu
    df_method3 = scraper.scrape_multiple_pages(
        keyword='laptop gaming',  # Lebih spesifik
        max_pages=3,
        delay=(2, 4),
        min_price=5000000,
        exclude_keywords=['tas', 'case', 'mouse', 'cooler']
    )
    
    # ============================================================
    # Pilih DataFrame mana yang mau dipakai
    # ============================================================
    df = df_method2  # Ganti sesuai kebutuhan
    
    df = scraper.scrape_multiple_pages(
    keyword='laptop',
    max_pages=100,
    min_price=2800000,      # Laptop jarang < 3 juta
    max_price=50000000,     # Batas atas wajar
    filter_keywords=[       # Hanya brand laptop
        'asus', 'lenovo', 'hp', 'dell', 'acer', 'msi',
        'apple', 'macbook', 'thinkpad', 'ideapad', 
        'vivobook', 'zenbook', 'rog', 'tuf', 'predator', 
        'legion', 'pavilion', 'inspiron', 'vostro'
    ],
    exclude_keywords=[      # Exclude accessories
        'tas', 'case', 'mouse', 'keyboard', 'charger',
        'cooler', 'stand', 'ram', 'ssd', 'speaker',
        'hub', 'adaptor', 'cable', 'sleeve', 'cover', 'hdmi', 'power bank'
      ]
    )
    
    if not df.empty:
        # Show sample data
        print("\n📋 Sample Data:")
        print(df[['name', 'price_text', 'shop_name', 'rating']].head(10).to_string())
        
        # Show statistics
        print(f"\n📊 Statistics:")
        print(f"   • Total products: {len(df)}")
        print(f"   • Average price: Rp {df['price'].mean():,.0f}")
        print(f"   • Price range: Rp {df['price'].min():,.0f} - Rp {df['price'].max():,.0f}")
        print(f"   • Unique shops: {df['shop_name'].nunique()}")
        
        # Save to CSV and Excel
        scraper.save_to_csv(df, 'laptops_filtered.csv')
        scraper.save_to_excel(df, 'laptops_filtered.xlsx')
        
        return df
    else:
        print("❌ No data scraped!")
        return None


if __name__ == "__main__":
    df = main()