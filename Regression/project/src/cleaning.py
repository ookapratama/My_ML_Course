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
  if pd.isna(text):
      return None
  match = re.search(r'(\d+)\s*GB', text.upper())
  return int(match.group(1)) if match else None


def extract_storage(text):
  if pd.isna(text):
      return None
  text = text.upper()

  # Try to catch numbers like 256GB, 512 GB, 1TB
  match_gb = re.search(r'(\d+)\s*GB', text)
  match_tb = re.search(r'(\d+)\s*TB', text)

  if match_tb:
      return int(match_tb.group(1)) * 1024  # convert TB → GB
  if match_gb:
      return int(match_gb.group(1))
  return None


def extract_cpu_brand(cpu):
  if pd.isna(cpu):
      return None
  cpu = cpu.upper()
  if "RYZEN" in cpu or "AMD" in cpu:
      return "AMD"
  if "INTEL" in cpu or "I3" in cpu or "I5" in cpu or "I7" in cpu or "I9" in cpu:
      return "Intel"
  return "Unknown"


def extract_cpu_model(cpu):
  if pd.isna(cpu):
      return None
  cpu = cpu.upper()

  match = re.search(r'(I3|I5|I7|I9|RYZEN\s*\d)', cpu)
  return match.group(0) if match else None


def clean_dataset(path = ''):
  df = pd.read_csv(path)
  
  # drop column yang tidak perlu
  df_drop_clean = df.drop(['shop_tier', 'badge', 'rating'], axis=1)
  
  # print(df_drop_clean.columns)
  print('data yg null : ',df_drop_clean.isna().sum())
  print('info data : ', df_drop_clean.info())
  print('total data : ', len(df_drop_clean))
  
  # Clean price
  df_drop_clean["price_clean"] = df_drop_clean["price"].apply(clean_price)
  
  # Discount percentage
  df_drop_clean['discount_percentage'] = df_drop_clean.apply(lambda row: get_percentage_discount(row['price'], row['original_price']), axis=1)

  # Extract RAM & Storage
  # df["ram_gb"] = df["name"].apply(extract_ram)
  # df["storage_gb"] = df["name"].apply(extract_storage)

  # # CPU features
  # df["cpu_brand"] = df["name"].apply(extract_cpu_brand)
  # df["cpu_model"] = df["name"].apply(extract_cpu_model)

  # # Remove missing prices
  # df = df[df["price_clean"].notnull()]

  # df.to_csv("../data/processed/laptops_clean.csv", index=False)
  # df.to_excel("../data/processed/laptops_clean.xlsx", index=False)
  # print("Saved cleaned dataset → data/processed/laptops_clean.csv")

  return df


if __name__ == "__main__":
  clean_dataset("../data/raw/laptops_filtered.csv")
