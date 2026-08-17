# 📘 Dokumentasi Hasil Belajar Regression Machine Learning

## 🎯 Tujuan Pembelajaran
Memahami berbagai jenis **model regresi** dalam machine learning, cara kerja, kelebihan, kekurangan, serta kapan dan bagaimana menggunakannya berdasarkan karakteristik data.

---

## 🧠 Model-Model yang Telah Dipelajari

### 1. Simple Linear Regression
- **Konsep:** Memprediksi nilai target berdasarkan satu fitur (variabel independen).
- **Contoh:** Memprediksi harga rumah berdasarkan luas tanah.
- **Kelebihan:** Mudah diinterpretasikan dan sangat cepat dilatih.
- **Kelemahan:** Tidak cocok untuk hubungan non-linear antar variabel.

---

### 2. Multiple Linear Regression
- **Konsep:** Sama seperti simple linear, namun menggunakan lebih dari satu fitur.
- **Contoh:** Memprediksi harga rumah berdasarkan luas tanah, jumlah kamar, dan lokasi.
- **Kelebihan:** Menangkap pengaruh simultan dari banyak fitur.
- **Kelemahan:** Sensitif terhadap multikolinearitas (fitur yang saling berkorelasi tinggi).

---

### 3. Polynomial Regression
- **Konsep:** Menambahkan pangkat (derajat) dari fitur untuk menangkap pola non-linear.
- **Contoh:** Prediksi pertumbuhan populasi yang tidak linear terhadap waktu.
- **Kelebihan:** Bisa memodelkan hubungan non-linear dengan pendekatan sederhana.
- **Kelemahan:** Mudah **overfitting** jika derajat polinomial terlalu tinggi.

---

### 4. Support Vector Regression (SVR)
- **Konsep:** Versi regresi dari SVM yang berusaha mencari garis (atau hyperplane) dengan margin kesalahan minimal.
- **Contoh:** Prediksi harga saham atau nilai ekonomi dengan batas toleransi error tertentu.
- **Kelebihan:** Tahan terhadap outlier, efektif pada data non-linear dengan kernel.
- **Kelemahan:** Lebih lambat di dataset besar dan sulit di-tuning.

---

### 5. Decision Tree Regression
- **Konsep:** Memecah data menjadi cabang-cabang berdasarkan kondisi hingga mencapai nilai prediksi.
- **Contoh:** Prediksi nilai properti berdasarkan kombinasi fitur kategorikal dan numerik.
- **Kelebihan:** Mudah diinterpretasikan dan tidak butuh normalisasi data.
- **Kelemahan:** Mudah **overfitting** jika tidak dilakukan pruning.

---

### 6. Random Forest Regression
- **Konsep:** Menggabungkan banyak Decision Tree untuk menghasilkan prediksi rata-rata.
- **Contoh:** Prediksi hasil panen, harga kendaraan, atau data kompleks lainnya.
- **Kelebihan:** Akurasi tinggi, stabil, dan tahan terhadap outlier.
- **Kelemahan:** Interpretasi hasil lebih sulit dibandingkan model tunggal.

---

## 🧩 Kesimpulan Pembelajaran

- Regresi digunakan ketika **target output berbentuk nilai kontinu (numerik)**.
- Setiap model memiliki kekuatan dan kelemahan — **tidak ada model terbaik secara universal**, tergantung pada data dan tujuan.
- Model sederhana (Linear, Polynomial) lebih cocok untuk data dengan pola yang jelas dan mudah dijelaskan.
- Model kompleks (SVR, Random Forest) lebih cocok untuk data besar dan non-linear.
- **Evaluasi performa model** bisa menggunakan metrik seperti:
  - `MAE` (Mean Absolute Error)
  - `MSE` (Mean Squared Error)
  - `RMSE` (Root Mean Squared Error)
  - `R²` (Coefficient of Determination)

---

## 🧭 Panduan Pemilihan Model di Kasus Regresi

| Kondisi Dataset | Model yang Disarankan | Catatan |
|------------------|------------------------|----------|
| Pola linear sederhana | Simple / Multiple Linear | Cocok untuk data dengan hubungan linear jelas |
| Pola non-linear ringan | Polynomial | Sesuaikan derajat agar tidak overfitting |
| Pola non-linear kompleks | SVR / Random Forest | Gunakan jika hubungan sulit dimodelkan secara linear |
| Banyak fitur dan noise | Random Forest | Stabil terhadap data berisik |
| Data sedikit, sederhana | Linear Regression | Cepat dan efisien |
| Fitur campuran (numerik + kategorikal) | Decision Tree / Random Forest | Tidak perlu scaling data |

---

## 🧮 Cara Menentukan Bahwa Dataset Menggunakan Regresi

Gunakan **regresi** jika target (label) memenuhi kondisi berikut:

- Nilainya **kontinu**, bukan kategori.
- Contoh:
  - Harga rumah (`Rp`)
  - Suhu (`°C`)
  - Jumlah penjualan (`unit`)
  - Tingkat kepuasan (`0–10`)

Jika target berupa **kategori atau label diskrit**, maka itu termasuk **klasifikasi**, bukan regresi.

---

## 🚀 Rencana Pembelajaran Selanjutnya

1. **Pelajari evaluasi dan tuning model:**
   - Hyperparameter tuning (Grid Search, Random Search)
   - Cross-validation
2. **Eksperimen dengan dataset nyata (misal: Kaggle atau UCI Machine Learning Repository).**
3. **Pelajari Regularization:**
   - Ridge, Lasso, dan ElasticNet Regression.
4. **Mulai memahami regresi lanjutan:**
   - Gradient Boosting, XGBoost, dan LightGBM.

---

## 📝 Catatan Penting

- Selalu lakukan **eksplorasi data (EDA)** sebelum memilih model.
- Periksa **korelasi antar fitur** untuk menghindari multikolinearitas.
- Gunakan **visualisasi residual** untuk melihat apakah model sudah cocok.
- Jangan hanya fokus pada akurasi — pertimbangkan **interpretabilitas dan efisiensi**.

---