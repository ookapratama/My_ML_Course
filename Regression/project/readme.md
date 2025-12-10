# 💻 Prediksi Harga Laptop Menggunakan Machine Learning  
Proyek ini adalah sistem prediksi harga laptop berbasis *machine learning* yang dibangun dari awal, mulai dari scraping data e-commerce, pembersihan data, eksplorasi data, pemodelan regresi, tuning model, hingga deployment menggunakan Streamlit Cloud.

Project ini dirancang sebagai portofolio profesional untuk menunjukkan kemampuan dalam:

- Data scraping (Tokopedia GraphQL API)
- Data cleaning & feature engineering
- Exploratory Data Analysis (EDA)
- Model regresi (Linear Regression, Random Forest, XGBoost)
- Hyperparameter tuning
- Deployment model ML
- Penerapan end-to-end machine learning workflow

---

## **🛠 Teknologi yang Digunakan**

| Teknologi | Logo |
|-----------|------|
| **Python** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **Pandas** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) |
| **NumPy** | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) |
| **Scikit-Learn** | ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) |
| **XGBoost** | ![XGBoost](https://img.shields.io/badge/XGBoost-FF6F00?style=for-the-badge&logo=xgboost&logoColor=white) |
| **Matplotlib** | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white) |
| **Seaborn** | ![Seaborn](https://img.shields.io/badge/Seaborn-5599FF?style=for-the-badge) |
| **Streamlit** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) |
| **Tokopedia GraphQL API** | ![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white) |

---

## 🚀 **Fitur Project**

### ✔ 1. Data Scraping
- Data dikumpulkan dari Tokopedia menggunakan GraphQL API.
- Filtering dilakukan untuk memastikan hanya laptop asli (bukan aksesori) yang ikut dalam dataset.

### ✔ 2. Data Cleaning & Feature Engineering
- Ekstraksi RAM (GB)
- Ekstraksi Storage (GB)
- Klasifikasi CPU (i3/i5/i7/i9, Ryzen series, Apple M-series)
- Penanganan missing values
- Encoding CPU series

### ✔ 3. Exploratory Data Analysis (EDA)
Visualisasi meliputi:
- Distribusi harga
- Korelasi antar fitur (heatmap)
- Boxplot harga berdasarkan CPU series
- Scatter plot RAM/Storage terhadap harga
- Statistik per brand dan CPU

### ✔ 4. Model Training
Model yang diuji:
- Linear Regression
- Random Forest Regressor
- XGBoost Regressor → **model terbaik**

### ✔ 5. Hyperparameter Tuning
Dilakukan untuk meningkatkan performa:
- RandomizedSearchCV
- GridSearchCV

### ✔ 6. Evaluasi Model
Metrik yang digunakan:
- MAE
- RMSE
- R² Score  
XGBoost memberikan hasil terbaik.

### ✔ 7. Deployment
- Model diexport menggunakan `joblib`
- Aplikasi prediksi dibangun menggunakan Streamlit
- Deployment ke Streamlit Cloud

---

## 🗂 **Struktur Folder Project**

project/
│── data/
│ ├── raw/
│ ├── processed/
│
│── src/
│ ├── scraper.py
│ ├── cleaning.py
│ ├── preprocessing.py
│ ├── train_model.py
│ ├── feature_engineering.py
│ ├── hyperparameter.py
│ ├── evaluate_models.py
│
│── models/
│ ├── traditional/
│ │ ├── xgboost.pkl
│ ├── cpu_series_encoder.pkl
│
│── notebooks/
│ ├── scraping.ipynb
│ ├── cleaning.ipynb
│ ├── eda.ipynb
│ ├── modeling.ipynb
│ ├── hyperparameter.ipynb
│
│── app/
│ ├── app.py # Streamlit UI
│
│── requirements.txt
│── README.md

---

## 📊 **Hasil Evaluasi Model**

| Model              | MAE          | RMSE        | R² Score |
|-------------------|--------------|-------------|----------|
| Linear Regression | 2.73 juta    | besar       | 0.71     |
| Random Forest     | 2.45 juta    | lebih kecil | 0.75     |
| **XGBoost**       | **2.44 juta**| **terbaik** | **0.76** |

**Kesimpulan:**  
XGBoost memberikan performa terbaik dan digunakan sebagai model final untuk deployment.

---

## 🧠 **Cara Menjalankan Proyek Secara Lokal**

### 1️⃣ Clone Repository
```bash
git clone https://github.com/username/project-laptop-price
cd project-laptop-price
pip install -r requirements.txt
streamlit run app/app.py
```

### Demo Aplikasi
👉 Live Demo (Streamlit Cloud): https://ookapratama-my-ml-course-regressionprojectappapp-jav0la.streamlit.app/

## **Input yang didukung Model**
- Brand
- CPU Series
- CPU Brand
- RAM (GB)
- Storage (GB)

## Author
Nama: Ooka Pratama
Website Portofolio : https://ooka.my.id/
Portofolio GitHub: https://github.com/ookapratama/
Email: ookapratama@gmail.com