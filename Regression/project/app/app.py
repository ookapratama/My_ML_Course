import os
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))   # → path ke /app
PROJECT_ROOT = os.path.dirname(ROOT)                # → path ke /project
MODEL_DIR = os.path.join(PROJECT_ROOT, "models", "traditional")
  
import streamlit as st
import joblib
import pandas as pd
from src.preprocessing import preprocess_input


# Load model
# model = joblib.load("/home/ooka/BACKUP ARCH/jinx/Belajar/ML udemy/Regression/project/models/traditional/xgboost.pkl")
# model = joblib.load("../models/traditional/xgboost.pkl")
model_path = os.path.join(MODEL_DIR, "xgboost.pkl")
model = joblib.load(model_path)


# Load encoder (cpu_series → integer)
# encoder_cpu_series = joblib.load("../models/cpu_series_encoder.pkl")

st.title("💻 Prediksi Harga Laptop")
st.write("Masukkan spesifikasi laptop untuk memprediksi harganya.")

# Input form
brand = st.selectbox("Brand Laptop", ["Asus", "Acer", "Dell", "HP", "Lenovo", "MSI", "Apple", "Other"])
cpu_series = st.selectbox("CPU Series", ["i3", "i5", "i7", "i9", "Ryzen 3", "Ryzen 5", "Ryzen 7", "M1", "M2", "M3"])
cpu_brand = st.selectbox("CPU Brand", ["Intel", "AMD", "Apple"])
ram_gb = st.selectbox("RAM (GB)", [4, 8, 16, 32, 64])
storage_gb = st.selectbox("Storage (GB)", [128, 256, 512, 1024, 2048])

# Predict
if st.button("Prediksi Harga"):
  input_data = {
      "brand": brand,
      "cpu_series": cpu_series,
      "cpu_brand": cpu_brand,
      "ram_gb": ram_gb,
      "storage_gb": storage_gb,
  }

  df_preprocessed = preprocess_input(input_data)

  prediction = model.predict(df_preprocessed)[0]

  st.success(f"💰 Prediksi Harga: Rp {prediction:,.0f}")
