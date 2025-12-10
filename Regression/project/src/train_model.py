import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import joblib

# load dataset
df = pd.read_csv("../data/processed/laptops_clean.csv")
df_new = df.drop('original_price', axis=1)
# print(df_new.head())

# Selecting fitur
features = [
    'cpu_brand',
    'cpu_series',
    'ram_gb',
    'storage_gb',
]

target = 'price_clean'

# Split dataset
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Preprocessing pipelin
categorical_cols = ['cpu_brand', 'cpu_series']
numeric_cols = ['ram_gb', 'storage_gb']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
        ('num', StandardScaler(), numeric_cols)
    ]
)

# Define Models
from xgboost import XGBRegressor
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        random_state=42
    ),
    "XGBoost": XGBRegressor(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        tree_method="hist"
    )
}


# Train & Evaluate Models
results = []

if not os.path.exists("../models/traditional/"):
    os.makedirs("../models/traditional/")

for name, model in models.items():

    print(f"\nTraining {name}...")

    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    results.append([name, mae, rmse, r2])

    # Save model
    # file_path = f"../models/traditional/{name.replace(' ', '_').lower()}.pkl"
    # joblib.dump(pipeline, file_path)

    # print(f"Saved model: {file_path}")
    print(f"MAE: {mae:,.0f}")
    print(f"RMSE: {rmse:,.0f}")
    print(f"R2: {r2:.3f}")

# Save result models
results_df = pd.DataFrame(results, columns=["Model", "MAE", "RMSE", "R2"])
# results_df.to_csv("../models/model_results.csv", index=False)

print("\n=== Training Complete! ===")
print(results_df)


