import joblib
import pandas as pd

def preprocess_input(data):
  df = pd.DataFrame([data])

  # Pastikan kolom sudah bersih
  df["ram_gb"] = df["ram_gb"].astype(int)
  df["storage_gb"] = df["storage_gb"].astype(int)

  return df
