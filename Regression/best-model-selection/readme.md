# 📚 Quick Usage Guide

> 🚀 **Machine Learning Framework** — a simple, modular, and extensible notebook for data analysis, model comparison, and automated evaluation.

---

## 🧩 How to Use This Framework (index.ipynb)

### 1️⃣ Prepare Your Data
📁 **Requirements:**
- Format: `.csv` file with **features + target (last column)**
- No missing values (will be auto-filled with mean)
- Place file at: `dataset/Data.csv`

---

### 2️⃣ Run the Framework
💡 **Steps:**
1. Execute all notebook cells **sequentially** (Cell 1 → Cell 13)
2. The framework will automatically:
   - 🧹 Load & explore data  
   - 🤖 Train **7 different models**  
   - 📊 Evaluate and compare performance  
   - 🎨 Generate visualizations  
   - 💾 Save the **best-performing model**

⏱ **Estimated runtime:** 2–5 minutes (depends on dataset size)

---

### 3️⃣ Interpret Results
📈 **Evaluation Tips:**
- **R² (Coefficient of Determination):** Closer to **1.0** = better  
- **RMSE / MAE:** Closer to **0** = better  
- Review visualizations for further insights

---

### 4️⃣ Use the Best Model
💾 **Model saved in:** `models/best_model_*.pkl`

Use the helper function to make predictions:

```python
features = np.array([[val1, val2, val3, ...]])
prediction = predict_with_best_model(features)
```