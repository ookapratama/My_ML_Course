import streamlit as st
import joblib
import pandas as pd
from src.preprocessing import preprocess_input

# Load model
model = joblib.load("model/best_model.pkl")

# Load encoder (cpu_series → integer)
encoder_cpu_series = joblib.load("model/cpu_series_encoder.pkl")

st.title("💻 Prediksi Harga Laptop")
st.write("Masukkan spesifikasi laptop untuk memprediksi harganya.")

# Input form
brand = st.selectbox("Brand Laptop", ["Asus", "Acer", "Dell", "HP", "Lenovo", "MSI", "Apple", "Other"])
cpu_series = st.selectbox("CPU Series", ["i3", "i5", "i7", "i9", "Ryzen 3", "Ryzen 5", "Ryzen 7", "M1", "M2", "M3"])
ram_gb = st.selectbox("RAM (GB)", [4, 8, 16, 32, 64])
storage_gb = st.selectbox("Storage (GB)", [128, 256, 512, 1024, 2048])

# Predict
if st.button("Prediksi Harga"):
  input_data = {
      "brand": brand,
      "cpu_series": cpu_series,
      "ram_gb": ram_gb,
      "storage_gb": storage_gb,
  }

  df_preprocessed = preprocess_input(input_data, encoder_cpu_series)

  prediction = model.predict(df_preprocessed)[0]

  st.success(f"💰 Prediksi Harga: Rp {prediction:,.0f}")
