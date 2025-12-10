import pandas as pd

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from xgboost import XGBRegressor
import numpy as np
import joblib

# ===============================
# Load data
# ===============================
df = pd.read_csv("../data/processed/laptops_clean.csv")

print(f"Original data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Preprocessing non numerik data
X = df[['ram_gb', 'storage_gb', 'cpu_series', 'storage_type', 'cpu_brand']]
y = df["price_clean"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define Preprocessor
categorical_cols = ['cpu_series', 'storage_type','cpu_brand']
numeric_cols = ['ram_gb', 'storage_gb']

preprocessor = ColumnTransformer(
  transformers=[
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
    ('num', StandardScaler(), numeric_cols)
  ]
)


# ===============================
# Random Forest Hyperparameter Space
# ===============================
rf_pipeline = Pipeline(steps=[
  ('preprocessor', preprocessor),
  ('model', RandomForestRegressor(random_state=42))
])

rf_params = {
  "model__n_estimators": [200, 400, 600, 800, 1000],
  "model__max_depth": [10, 20, 30, 40, None],
  "model__min_samples_split": [2, 5, 10, 15],
  "model__min_samples_leaf": [1, 2, 4, 6],
  "model__max_features": ['auto', "sqrt", "log2"]
}

rf_search = RandomizedSearchCV(
  rf_pipeline,
  rf_params,
  n_iter=20,
  scoring="neg_mean_absolute_error",
  cv=5,
  verbose=2,
  random_state=42,
  n_jobs=-1,
  refit=True
)

print("🔍 Running Random Forest tuning...")
rf_search.fit(X_train, y_train)

best_rf = rf_search.best_estimator_
# print("Best RF params:", rf_search.best_params_)

# Evaluate
rf_pred = best_rf.predict(X_test)
print("RF MAE:", mean_absolute_error(y_test, rf_pred))
print("RF R2:", r2_score(y_test, rf_pred))

# joblib.dump(best_rf, "../models/hyperparameter/best_rf.pkl")
print("✔ Saved best RF model")


# ===============================
# XGBoost Hyperparameter Space
# ===============================
xgb_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', XGBRegressor(objective="reg:squarederror", random_state=42))
])

xgb_params = {
    "model__n_estimators": [200, 400, 600, 800],
    "model__learning_rate": [0.01, 0.05, 0.1, 0.2],
    "model__max_depth": [3, 5, 7, 10],
    "model__subsample": [0.6, 0.8, 1.0],
    "model__colsample_bytree": [0.6, 0.8, 1.0],
    "model__gamma": [0, 1, 3, 5],
    "model__min_child_weight": [1, 3, 5]
}

xgb_search = RandomizedSearchCV(
    xgb_pipeline,
    xgb_params,
    n_iter=20,
    scoring="neg_mean_absolute_error",
    cv=3,
    verbose=2,
    random_state=42,
    n_jobs=-1
)

print("\n🔍 Running XGBoost tuning...")
xgb_search.fit(X_train, y_train)

best_xgb = xgb_search.best_estimator_
# print("Best XGB params:", xgb_search.best_params_)

# Evaluate
xgb_pred = best_xgb.predict(X_test)
print("XGB MAE:", mean_absolute_error(y_test, xgb_pred))
print("XGB R2:", r2_score(y_test, xgb_pred))

# joblib.dump(best_xgb, "../models/hyperparameter/best_xgb.pkl")
print("✔ Saved best XGBoost model")


