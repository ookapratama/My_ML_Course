import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate(model, X_test, y_test):
    """Return MAE, RMSE, R2"""
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    return mae, rmse, r2, preds


def main():
    print("🔍 Loading dataset...")
    df = pd.read_csv("../data/processed/laptops_clean.csv")

    # Pastikan split konsisten dengan train_model.py
    from sklearn.model_selection import train_test_split

    features = [
      'cpu_brand',
      'cpu_series',
      'ram_gb',
      'storage_gb',
    ]

    X = df[features]
    y = df['price_clean']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("📦 Loading saved models...")
    models = {
        'Linear Regression': joblib.load("../models/traditional/linear_regression.pkl"),
        'Random Forest': joblib.load("../models/traditional/random_forest.pkl"),
        'XGBoost': joblib.load("../models/traditional/xgboost.pkl"),
    }

    results = []

    print("\n📊 Evaluating models...")
    for name, model in models.items():
        mae, rmse, r2, preds = evaluate(model, X_test, y_test)

        print(f"\n===== {name} =====")
        print(f"MAE  : {mae:,.0f}")
        print(f"RMSE : {rmse:,.0f}")
        print(f"R²   : {r2:.4f}")

        results.append({
            "model": name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        })

    df_results = pd.DataFrame(results)
    # df_results.to_csv("../models/model_evaluation_results.csv", index=False)

    print("\n📁 Results saved to: models/model_evaluation_results.csv")

    # Optional: show prediction sample
    print("\n🔍 Sample predictions:")
    sample = X_test.iloc[:5]
    for name, model in models.items():
        preds = model.predict(sample)
        print(f"\n{name} predictions:")
        print(preds)

    return df_results


if __name__ == "__main__":
    main()
