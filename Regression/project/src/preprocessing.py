import joblib
import pandas as pd

def preprocess_input(data, encoder_cpu_series):
  df = pd.DataFrame([data])

  # Pastikan kolom sudah bersih
  df["ram_gb"] = df["ram_gb"].astype(int)
  df["storage_gb"] = df["storage_gb"].astype(int)

  # CPU encoding (matching training)
  df["cpu_series_encoded"] = df["cpu_series"].map(encoder_cpu_series)

  # Handle missing kategori
  df["cpu_series_encoded"] = df["cpu_series_encoded"].fillna(encoder_cpu_series["Unknown"])

  return df
