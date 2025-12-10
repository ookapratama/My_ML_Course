import pandas as pd
import re

def clean_price(text):
  if pd.isna(text):
      return None
  text = re.sub(r'[^\d]', '', str(text))
  return int(text) if text.isdigit() else None

def get_percentage_discount(discount_price, real_price):
  # Set ke 0 jika tidak ada discount  
  real_price = 0 if pd.isna(real_price) else real_price   
  real_price = re.sub(r'[^\d]', '', str(real_price))
  
  # parse text harga ke nilai yg bisa di olah 
  discount_price = re.sub(r'[^\d]', '', str(discount_price))
  
  # get discount
  discount_percentage = round((int(real_price) - int(discount_price)) / int(real_price) * 100, 2) if real_price != '0' else 100
  return discount_percentage

def extract_ram(text):
  """
  Extract RAM size dari nama produk laptop
  
  Supports berbagai format:
  - "8GB RAM", "16 GB"
  - "RAM 8GB", "RAM 16GB"
  - "8/512" (RAM/Storage format)
  - "DDR4 8GB", "8GB DDR5"
  - "[8GB]", "(16GB)"
  
  Returns:
      int: RAM size dalam GB, atau None jika tidak ditemukan
  """
  if pd.isna(text):
      return None
  
  text_upper = text.upper()
  
  # ================================================================
  # PATTERN 1: Standard "8GB", "16 GB" (dengan/tanpa spasi)
  # ================================================================
  # Cari: angka 1-2 digit + optional spasi + GB
  # Hindari: angka yang diikuti SSD/HDD/NVME/STORAGE (itu storage, bukan RAM)
  pattern1 = r'\b(\d{1,2})\s*GB\b(?!\s*(?:SSD|HDD|NVME|M\.?2|STORAGE))'
  matches = re.findall(pattern1, text_upper)
  
  # Validasi: ambil yang masuk range RAM laptop
  for match in matches:
      ram_value = int(match)
      if ram_value in [2, 4, 6, 8, 12, 16, 20, 24, 32, 48, 64]:
          return ram_value
  
  # ================================================================
  # PATTERN 2: Dengan kata "RAM" eksplisit
  # ================================================================
  # Format: "8GB RAM", "RAM 8GB", "RAM: 8GB"
  pattern2 = r'(?:RAM[\s:]*)?(\d{1,2})\s*GB[\s]*(?:RAM)?'
  matches2 = re.findall(pattern2, text_upper)
  
  for match in matches2:
      ram_value = int(match)
      if ram_value in [2, 4, 6, 8, 12, 16, 20, 24, 32, 48, 64]:
          return ram_value
  
  # ================================================================
  # PATTERN 3: Format "8/512" atau "16/1TB" (RAM/Storage)
  # ================================================================
  # Common di seller yang pakai format singkat
  pattern3 = r'\b(\d{1,2})[/\-](\d+)(?:GB|TB)?\b'
  match3 = re.search(pattern3, text_upper)
  
  if match3:
      first_num = int(match3.group(1))
      second_num = int(match3.group(2))
      
      # Logika: angka kecil biasanya RAM, angka besar storage
      if first_num in [2, 4, 6, 8, 12, 16, 20, 24, 32] and second_num >= 128:
          return first_num
  
  # ================================================================
  # PATTERN 4: DDR format "DDR4 8GB", "8GB DDR5"
  # ================================================================
  pattern4 = r'(?:DDR[3-5][\s]+)?(\d{1,2})\s*GB[\s]*(?:DDR[3-5])?'
  matches4 = re.findall(pattern4, text_upper)
  
  for match in matches4:
      ram_value = int(match)
      if ram_value in [2, 4, 6, 8, 12, 16, 20, 24, 32, 48, 64]:
          return ram_value
  
  # ================================================================
  # PATTERN 5: Format dalam bracket/parentheses "[8GB]", "(16GB)"
  # ================================================================
  pattern5 = r'[\[\(](\d{1,2})\s*GB[\]\)]'
  match5 = re.search(pattern5, text_upper)
  
  if match5:
      ram_value = int(match5.group(1))
      if ram_value in [2, 4, 6, 8, 12, 16, 20, 24, 32, 48, 64]:
          return ram_value
  
  # ================================================================
  # PATTERN 6: Format "MEM 8GB", "MEMORY 8GB"
  # ================================================================
  pattern6 = r'(?:MEM(?:ORY)?[\s:]+)?(\d{1,2})\s*GB'
  matches6 = re.findall(pattern6, text_upper)
  
  for match in matches6:
      ram_value = int(match)
      if ram_value in [2, 4, 6, 8, 12, 16, 20, 24, 32, 48, 64]:
          return ram_value
  
  # Tidak ditemukan
  return None

def fill_missing_ram(price):
  """
  Fill missing RAM berdasarkan harga
  
  Args:
      price: Harga laptop (Rupiah)
  
  Returns:
      int: RAM dalam GB
  """
  if pd.isna(price):
      return None
  
  # Rule berdasarkan harga pasar laptop Indonesia
  if price < 3000000:
      return 4
  elif price < 5000000:
      return 4
  elif price < 7000000:
      return 8
  elif price < 10000000:
      return 8
  elif price < 15000000:
      return 8
  elif price < 20000000:
      return 16
  elif price < 30000000:
      return 16
  else:
      return 32


def extract_storage(text):
  """
  Extract storage size dan type dari nama produk

  Returns:
      tuple: (storage_gb, storage_type)
      - storage_gb: int (dalam GB, sudah convert dari TB)
      - storage_type: str ('ssd', 'hdd', atau None)

  Examples:
      "Laptop 512GB SSD" -> (512, 'ssd')
      "Laptop 1TB HDD" -> (1024, 'hdd')
      "Laptop SSD 256GB" -> (256, 'ssd')
      "Laptop 8/512" -> (512, None)
  """
  if pd.isna(text):
      return None, None

  text_upper = text.upper()
  storage_gb = None
  storage_type = None

  # Pattern 1: "512GB SSD", "1TB NVMe", "256GB M.2"
  pattern1 = r'(\d+)\s*(GB|TB)\s+(SSD|NVME|M\.?2)'
  match1 = re.search(pattern1, text_upper)
  if match1:
      size = int(match1.group(1))
      unit = match1.group(2)
      storage_gb = size * 1024 if unit == 'TB' else size
      storage_type = 'ssd'
      return storage_gb, storage_type

  # Pattern 2: "SSD 512GB", "NVMe 1TB"
  pattern2 = r'(SSD|NVME|M\.?2)\s+(\d+)\s*(GB|TB)'
  match2 = re.search(pattern2, text_upper)
  if match2:
      size = int(match2.group(2))
      unit = match2.group(3)
      storage_gb = size * 1024 if unit == 'TB' else size
      storage_type = 'ssd'
      return storage_gb, storage_type

  # Pattern 3: "1TB HDD", "500GB HDD"
  pattern3 = r'(\d+)\s*(GB|TB)\s+(HDD|SATA)'
  match3 = re.search(pattern3, text_upper)
  if match3:
      size = int(match3.group(1))
      unit = match3.group(2)
      storage_gb = size * 1024 if unit == 'TB' else size
      storage_type = 'hdd'
      return storage_gb, storage_type

  # Pattern 4: "HDD 1TB"
  pattern4 = r'(HDD|SATA)\s+(\d+)\s*(GB|TB)'
  match4 = re.search(pattern4, text_upper)
  if match4:
      size = int(match4.group(2))
      unit = match4.group(3)
      storage_gb = size * 1024 if unit == 'TB' else size
      storage_type = 'hdd'
      return storage_gb, storage_type

  # Pattern 5: Format slash "8/512" (RAM/Storage)
  pattern5 = r'\b\d{1,2}[/\-](\d+)\b'
  match5 = re.search(pattern5, text_upper)
  if match5:
      size = int(match5.group(1))
      # Validasi: storage laptop biasanya 128, 256, 512, 1024, 2048
      if size in [128, 256, 512, 1024, 2048]:
          storage_gb = size
          storage_type = None  # Unknown
          return storage_gb, storage_type

  # Pattern 6: Standalone "512GB", "1TB" (tanpa SSD/HDD keyword)
  # Hanya ambil jika > 64GB (karena < 64GB kemungkinan RAM)
  pattern6 = r'\b(\d+)\s*(GB|TB)\b(?!\s*RAM)'
  matches6 = re.findall(pattern6, text_upper)
  for match in matches6:
      size = int(match[0])
      unit = match[1]
      
      # Validasi: harus > 64GB untuk dianggap storage
      if unit == 'GB' and size >= 128:
          storage_gb = size
          storage_type = None
          return storage_gb, storage_type
      elif unit == 'TB':
          storage_gb = size * 1024
          storage_type = None
          return storage_gb, storage_type

  return None, None

def fill_missing_storage(price):
  """
  Fill missing storage berdasarkan harga
  
  Args:
      price: Harga laptop (Rupiah)
  
  Returns:
      int: Storage dalam GB
  """
  if pd.isna(price):
      return None
  
  # Rule berdasarkan harga pasar laptop Indonesia
  if price < 3000000:
      return 128  # Entry level
  elif price < 5000000:
      return 256  # Budget
  elif price < 7000000:
      return 256  # Lower mid
  elif price < 10000000:
      return 512  # Mid-range
  elif price < 15000000:
      return 512  # Upper mid
  elif price < 20000000:
      return 512  # High-end
  elif price < 30000000:
      return 1024  # Premium (1TB)
  else:
      return 1024  # Ultra premium


def fill_missing_storage_type(price):
  """
  Fill missing storage type berdasarkan harga
  
  Args:
      price: Harga laptop (Rupiah)
  
  Returns:
      str: 'ssd' atau 'hdd'
  """
  if pd.isna(price):
      return None
  
  # Laptop > 5 juta biasanya sudah SSD
  if price < 5000000:
      return 'hdd'  # Budget masih pakai HDD
  else:
      return 'ssd'

# def extract_cpu_brand(cpu):
#   if pd.isna(cpu):
#       return None
#   cpu = cpu.upper()
#   if "RYZEN" in cpu or "AMD" in cpu:
#       return "AMD"
#   if "INTEL" in cpu or "I3" in cpu or "I5" in cpu or "I7" in cpu or "I9" in cpu:
#       return "Intel"
#   return "Unknown"


def extract_cpu_brand(text):
    """
    Extract CPU brand dari nama produk
    
    Returns:
        str: 'Intel', 'AMD', 'Apple', atau None
    """
    if pd.isna(text):
        return None
    
    text_upper = text.upper()
    
    # Intel
    if re.search(r'\b(INTEL|CORE\s+I[3579]|CELERON|PENTIUM)\b', text_upper):
        return 'Intel'
    
    # AMD
    if re.search(r'\b(AMD|RYZEN|ATHLON)\b', text_upper):
        return 'AMD'
    
    # Apple
    if re.search(r'\b(APPLE|M[123]\b|MACBOOK)\b', text_upper):
        return 'Apple'
    
    return None


def extract_cpu_model(text):
    """
    Extract CPU model dari nama produk
    
    Returns:
        str: Model CPU (e.g., 'i5-1135G7', 'Ryzen 5 5500U', 'M2', 'N4020')
    """
    if pd.isna(text):
        return None
    
    text_upper = text.upper()
    
    # Intel Core Ultra (handle dulu yang spesifik)
    # Pattern: Core Ultra 5 125H, Core Ultra 7 155H
    pattern_ultra = r'CORE\s+ULTRA\s+([579])\s+(\d{3,5}[A-Z]*)'
    match = re.search(pattern_ultra, text_upper)
    if match:
        return 'Core Ultra ' + match.group(1) + ' ' + match.group(2)
    
    # Intel Core i3/i5/i7/i9 dengan generasi
    # Pattern: i5-12450H, i7-13700H, Core i5-1135G7, i5 1135G7
    pattern_intel_core = r'(?:CORE\s+)?(I[3579])\s*-?\s*(\d{4,5}[A-Z]*)'
    match = re.search(pattern_intel_core, text_upper)
    if match:
        return match.group(1) + '-' + match.group(2)
    
    # Intel N-series (N4020, N5030, N100, N200, dll)
    # Pattern: N4020, N5030, N95, N100, N200
    pattern_n_series = r'\b(N\d{3,4}[A-Z]*)\b'
    match = re.search(pattern_n_series, text_upper)
    if match:
        return match.group(1)
    
    # Intel Celeron/Pentium (dengan model number)
    # Pattern: Celeron N4020, Pentium Silver N5030, Celeron 5205U
    pattern_celeron = r'(CELERON|PENTIUM)\s+(SILVER\s+|GOLD\s+)?([A-Z]?\d{3,5}[A-Z]*)'
    match = re.search(pattern_celeron, text_upper)
    if match:
        prefix = match.group(1)
        variant = match.group(2).strip() if match.group(2) else ''
        model = match.group(3)
        return f"{prefix} {variant} {model}".strip().replace('  ', ' ')
    
    # Intel Atom (jarang, tapi ada)
    # Pattern: Atom x5-Z8350
    pattern_atom = r'ATOM\s+([A-Z0-9\-]+)'
    match = re.search(pattern_atom, text_upper)
    if match:
        return 'Atom ' + match.group(1)
    
    # AMD Ryzen
    # Pattern: Ryzen 5 5500U, Ryzen 7 5800H, Ryzen 9 7940HS
    pattern_ryzen = r'RYZEN\s+([3579])\s+(\d{4}[A-Z]*)'
    match = re.search(pattern_ryzen, text_upper)
    if match:
        return 'Ryzen ' + match.group(1) + ' ' + match.group(2)
    
    # AMD Athlon
    # Pattern: Athlon Silver 3050U, Athlon Gold 3150U
    pattern_athlon = r'ATHLON\s+(SILVER\s+|GOLD\s+)?([A-Z0-9\-]+)'
    match = re.search(pattern_athlon, text_upper)
    if match:
        variant = match.group(1).strip() if match.group(1) else ''
        model = match.group(2)
        return f"Athlon {variant} {model}".strip().replace('  ', ' ')
    
    # Apple M1/M2/M3
    # Pattern: M1, M2 Pro, M3 Max, M3 Ultra
    pattern_apple = r'\b(M[123])\s*(PRO|MAX|ULTRA)?\b'
    match = re.search(pattern_apple, text_upper)
    if match:
        chip = match.group(1)
        variant = match.group(2) if match.group(2) else ''
        return (chip + ' ' + variant).strip()
    
    return None


def fill_missing_cpu_brand(price):
    """
    Fill missing CPU brand berdasarkan harga
    
    Args:
        price: Harga laptop (Rupiah)
    
    Returns:
        str: 'Intel', 'AMD', atau 'Apple'
    """
    if pd.isna(price):
        return None
    
    # Logic berdasarkan market share dan price point
    if price < 5000000:
        return 'Intel'  # Budget: Intel dominan (Celeron/Pentium/i3)
    elif price < 10000000:
        return 'Intel'  # Mid-range: Intel masih dominan
    elif price < 20000000:
        return 'Intel'  # High-end: Mix, tapi Intel lebih umum
    elif price < 30000000:
        return 'Intel'  # Premium: Intel i7/i9
    else:
        return 'Intel'  # Ultra premium: Mix Intel/Apple, default Intel


def fill_missing_cpu_model(price, cpu_brand=None):
    """
    Fill missing CPU model berdasarkan harga dan brand
    
    Args:
        price: Harga laptop (Rupiah)
        cpu_brand: CPU brand ('Intel', 'AMD', 'Apple')
    
    Returns:
        str: CPU model estimate
    """
    if pd.isna(price):
        return None
    
    # Jika brand tidak diketahui, assume Intel (paling umum)
    if pd.isna(cpu_brand):
        cpu_brand = 'Intel'
    
    if cpu_brand == 'Intel':
        if price < 3000000:
            return 'Celeron'
        elif price < 5000000:
            return 'i3-Gen10'
        elif price < 7000000:
            return 'i3-Gen11'
        elif price < 10000000:
            return 'i5-Gen11'
        elif price < 15000000:
            return 'i5-Gen12'
        elif price < 20000000:
            return 'i7-Gen12'
        elif price < 30000000:
            return 'i7-Gen13'
        else:
            return 'i9-Gen13'
    
    elif cpu_brand == 'AMD':
        if price < 5000000:
            return 'Ryzen 3'
        elif price < 10000000:
            return 'Ryzen 5'
        elif price < 20000000:
            return 'Ryzen 7'
        else:
            return 'Ryzen 9'
    
    elif cpu_brand == 'Apple':
        if price < 15000000:
            return 'M1'
        elif price < 25000000:
            return 'M2'
        else:
            return 'M3'
    
    return None

def extract_cpu_series(cpu_model):
    if not isinstance(cpu_model, str):
        return ""
    
    cpu_model = cpu_model.strip().upper()
    # print(cpu_model)
    # Pattern untuk Intel: i3, i5, i7, i9, N100, N150, dll.
    intel_pattern = r'\b(I[3579]|N[0-9]+[A-Z]*|CELERON|PENTIUM|ATOM|CORE\s*(?:ULTRA)?\s*[0-9]?)\b'
    # Pattern untuk AMD: Ryzen 3, Ryzen 5, Ryzen 7, Ryzen 9, Athlon, dll.
    amd_pattern = r'\b(RYZEN\s*[3579]?|ATHLON|RYZEN\s*AI\s*[0-9]?|RYZEN\s*(?:[0-9]+\s*)?[A-Z]*)\b'
    # Pattern untuk Apple: M1, M2, M3, M4
    apple_pattern = r'\b(M[1234])\b'
    
    # Cari Intel
    intel_match = re.search(intel_pattern, cpu_model, re.IGNORECASE)
    if intel_match:
        series = intel_match.group(1)
        # Rapikan: hilangkan spasi berlebih
        series = re.sub(r'\s+', ' ', series.strip())
        # Untuk "CORE ULTRA 7" -> "ULTRA 7"
        if "CORE ULTRA" in series.upper():
            series = series.replace("CORE ", "")
        return series.title()
    
    # Cari AMD
    amd_match = re.search(amd_pattern, cpu_model, re.IGNORECASE)
    if amd_match:
        series = amd_match.group(1)
        # Rapikan: hilangkan spasi berlebih
        series = re.sub(r'\s+', ' ', series.strip())
        # Untuk "RYZEN AI 7" -> "RYZEN AI 7" (tetap)
        return series.title()
    
    # Cari Apple
    apple_match = re.search(apple_pattern, cpu_model, re.IGNORECASE)
    if apple_match:
        return apple_match.group(1).upper()
    
    # Jika tidak ditemukan, kembalikan string kosong atau model asli
    return ""

def clean_dataset(path = ''):
  df = pd.read_csv(path)
  
  # drop column yang tidak perlu
  df = df.drop(['shop_tier', 'badge', 'rating', 'price_text','labels', 'image_url', 'product_url'], axis=1)
  
  # print(df.columns)
  print('data yg null : ',df.isna().sum())
  print('info data : ', df.info())
  print('total data : ', len(df))
  
  # Clean price
  df["price_clean"] = df["price"].apply(clean_price)
  # Discount percentage
  df['discount_percentage'] = df.apply(lambda row: get_percentage_discount(row['price'], row['original_price']), axis=1)

  # Extract RAM & Storage
  df["ram_gb"] = df["name"].apply(extract_ram)
  # Fill missing RAM
  df['ram_gb'] = df['ram_gb'].fillna(df['price'].apply(fill_missing_ram))
  df[['storage_gb', 'storage_type']] = df['name'].apply(lambda x: pd.Series(extract_storage(x)))
  # Fill missing Storage
  df['storage_gb'] = df['storage_gb'].fillna(df['price'].apply(fill_missing_storage))
  df['storage_type'] = df['storage_type'].fillna(df['price'].apply(fill_missing_storage_type))

  # # CPU features
  df["cpu_brand"] = df["name"].apply(extract_cpu_brand)
  df["cpu_model"] = df["name"].apply(extract_cpu_model)
  
  df['cpu_brand'] = df['cpu_brand'].fillna(df['price'].apply(fill_missing_cpu_brand))
  df['cpu_model'] = df.apply(
      lambda row: row['cpu_model'] if pd.notna(row['cpu_model']) 
      else fill_missing_cpu_model(row['price'], row['cpu_brand']), 
      axis=1
  )
  
  df['cpu_series'] = df['cpu_model'].apply(extract_cpu_series)
#   print('data yg null : ',df.isna().sum())
#   print('data yg null : ',df.isnull().sum())
  

  df.to_csv('../data/processed/laptops_clean.csv', index=False)
  df.to_excel("../data/processed/laptops_clean.xlsx", index=False)
  print("Saved cleaned dataset → data/processed/laptops_clean.csv")

  return df


if __name__ == "__main__":
  clean_dataset("../data/raw/laptops_filtered.csv")
