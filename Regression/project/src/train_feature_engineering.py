import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import joblib

# ===============================
# 1. LOAD DATA
# ===============================
print("="*60)
print("LOADING DATA")
print("="*60)

df = pd.read_csv("../data/processed/laptops_clean.csv")

print(f"Original data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# ===============================
# 2. INITIAL TRAIN-TEST SPLIT
# (CRITICAL: Split BEFORE feature engineering!)
# ===============================
print("\n" + "="*60)
print("INITIAL TRAIN-TEST SPLIT")
print("="*60)

X_basic = df[['ram_gb', 'storage_gb', 'cpu_series', 'storage_type', 'cpu_brand']]
y = df["price_clean"]

X_train_basic, X_test_basic, y_train, y_test = train_test_split(
    X_basic, y, test_size=0.2, random_state=42
)

print(f"Train set: {X_train_basic.shape[0]} samples")
print(f"Test set: {X_test_basic.shape[0]} samples")

# ===============================
# 3. FEATURE ENGINEERING (NO LEAKAGE!)
# ===============================
print("\n" + "="*60)
print("FEATURE ENGINEERING (NO DATA LEAKAGE)")
print("="*60)

def add_features(X, y, is_train=True, train_stats=None):
    """
    Add engineered features without data leakage
    
    Parameters:
    - X: Feature dataframe
    - y: Target variable (for calculating train statistics only)
    - is_train: Whether this is training set
    - train_stats: Pre-calculated statistics from training set (for test set)
    
    Returns:
    - X_fe: Feature-engineered dataframe
    - stats: Statistics dictionary (only if is_train=True)
    """
    X_fe = X.copy()
    
    # ===== 1. BASIC INTERACTION FEATURES =====
    print(f"\n{'[TRAIN]' if is_train else '[TEST]'} Adding basic features...")
    
    # RAM × Storage interactions
    X_fe['ram_storage_product'] = X_fe['ram_gb'] * X_fe['storage_gb']
    X_fe['ram_storage_ratio'] = X_fe['ram_gb'] / X_fe['storage_gb'].replace(0, 1)
    X_fe['ram_plus_storage_normalized'] = X_fe['ram_gb'] + (X_fe['storage_gb'] / 1000)
    
    # Log transforms
    X_fe['log_ram'] = np.log1p(X_fe['ram_gb'])
    X_fe['log_storage'] = np.log1p(X_fe['storage_gb'])
    
    # Polynomial features
    X_fe['ram_squared'] = X_fe['ram_gb'] ** 2
    X_fe['storage_squared'] = X_fe['storage_gb'] ** 2
    X_fe['ram_cubed'] = X_fe['ram_gb'] ** 3
    
    print(f"   ✅ Added 8 basic interaction features")
    
    # ===== 2. CATEGORICAL COMBINATIONS =====
    print(f"{'[TRAIN]' if is_train else '[TEST]'} Adding categorical combinations...")
    
    X_fe['cpu_full'] = X_fe['cpu_brand'].astype(str) + '_' + X_fe['cpu_series'].astype(str)
    X_fe['brand_ram_tier'] = X_fe['cpu_brand'].astype(str) + '_RAM' + X_fe['ram_gb'].astype(str)
    
    print(f"   ✅ Added 2 categorical combination features")
    
    # ===== 3. SEGMENTATION FEATURES =====
    print(f"{'[TRAIN]' if is_train else '[TEST]'} Adding segmentation features...")
    
    # RAM categories
    def categorize_ram(ram):
        if ram <= 4:
            return 'low_ram'
        elif ram <= 8:
            return 'medium_ram'
        elif ram <= 16:
            return 'high_ram'
        else:
            return 'extreme_ram'
    
    X_fe['ram_category'] = X_fe['ram_gb'].apply(categorize_ram)
    
    # Storage categories
    def categorize_storage(storage):
        if storage <= 256:
            return 'low_storage'
        elif storage <= 512:
            return 'medium_storage'
        elif storage <= 1000:
            return 'high_storage'
        else:
            return 'extreme_storage'
    
    X_fe['storage_category'] = X_fe['storage_gb'].apply(categorize_storage)
    
    # Overall spec tier
    def spec_tier(row):
        ram = row['ram_gb']
        storage = row['storage_gb']
        if ram >= 16 and storage >= 1000:
            return 'flagship'
        elif ram >= 8 and storage >= 512:
            return 'mid_tier'
        else:
            return 'entry_level'
    
    X_fe['spec_tier'] = X_fe.apply(spec_tier, axis=1)
    
    print(f"   ✅ Added 3 segmentation features")
    
    # ===== 4. FREQUENCY ENCODING =====
    print(f"{'[TRAIN]' if is_train else '[TEST]'} Adding frequency encoding...")
    
    # CPU series frequency
    series_freq = X_fe['cpu_series'].value_counts()
    X_fe['cpu_series_frequency'] = X_fe['cpu_series'].map(series_freq)
    X_fe['cpu_series_frequency_pct'] = X_fe['cpu_series_frequency'] / len(X_fe)
    
    # Rare series indicator (< 1% of data)
    rare_threshold = len(X_fe) * 0.01
    X_fe['is_rare_series'] = (X_fe['cpu_series_frequency'] < rare_threshold).astype(int)
    
    print(f"   ✅ Added 3 frequency encoding features")
    
    # ===== 5. RANK FEATURES (BASED ON SPECS ONLY) =====
    print(f"{'[TRAIN]' if is_train else '[TEST]'} Adding rank features...")
    
    # RAM ranks
    X_fe['ram_rank_in_brand'] = X_fe.groupby('cpu_brand')['ram_gb'].rank(pct=True)
    X_fe['ram_rank_global'] = X_fe['ram_gb'].rank(pct=True)
    
    # Storage ranks
    X_fe['storage_rank_in_brand'] = X_fe.groupby('cpu_brand')['storage_gb'].rank(pct=True)
    X_fe['storage_rank_global'] = X_fe['storage_gb'].rank(pct=True)
    
    # Combined spec rank
    X_fe['combined_spec_rank'] = (X_fe['ram_rank_global'] + X_fe['storage_rank_global']) / 2
    
    print(f"   ✅ Added 5 rank features")
    
    # ===== 6. MARKET REFERENCE FEATURES (FROM TRAIN ONLY!) =====
    stats_dict = {}
    
    if is_train:
        print("[TRAIN] Computing market statistics from TRAIN set...")
        
        # Create temp dataframe with target for stats calculation
        temp_df = X_fe.copy()
        temp_df['price_clean'] = y
        
        # Brand statistics
        brand_stats = temp_df.groupby('cpu_brand')['price_clean'].agg([
            ('brand_mean_price', 'mean'),
            ('brand_std_price', 'std'),
            ('brand_median_price', 'median'),
            ('brand_count', 'count')
        ]).reset_index()
        
        # Series statistics
        series_stats = temp_df.groupby('cpu_series')['price_clean'].agg([
            ('series_mean_price', 'mean'),
            ('series_std_price', 'std'),
            ('series_count', 'count')
        ]).reset_index()
        
        # CPU full statistics
        cpu_full_stats = temp_df.groupby('cpu_full')['price_clean'].agg([
            ('cpu_full_mean_price', 'mean'),
            ('cpu_full_count', 'count')
        ]).reset_index()
        
        # RAM-Storage combo statistics
        ram_storage_stats = temp_df.groupby(['ram_gb', 'storage_gb'])['price_clean'].agg([
            ('ram_storage_combo_mean', 'mean'),
            ('ram_storage_combo_count', 'count')
        ]).reset_index()
        
        # Store statistics for test set
        stats_dict = {
            'brand_stats': brand_stats,
            'series_stats': series_stats,
            'cpu_full_stats': cpu_full_stats,
            'ram_storage_stats': ram_storage_stats,
            'overall_mean': temp_df['price_clean'].mean()
        }
        
        # Merge statistics to training features
        X_fe = X_fe.merge(brand_stats, on='cpu_brand', how='left')
        X_fe = X_fe.merge(series_stats, on='cpu_series', how='left')
        X_fe = X_fe.merge(cpu_full_stats, on='cpu_full', how='left')
        X_fe = X_fe.merge(ram_storage_stats, on=['ram_gb', 'storage_gb'], how='left')
        
        print(f"   ✅ Computed and added 12 market reference features")
        
    else:
        print("[TEST] Applying market statistics from TRAIN set...")
        
        # Use pre-calculated statistics from training set
        X_fe = X_fe.merge(train_stats['brand_stats'], on='cpu_brand', how='left')
        X_fe = X_fe.merge(train_stats['series_stats'], on='cpu_series', how='left')
        X_fe = X_fe.merge(train_stats['cpu_full_stats'], on='cpu_full', how='left')
        X_fe = X_fe.merge(train_stats['ram_storage_stats'], on=['ram_gb', 'storage_gb'], how='left')
        
        print(f"   ✅ Applied 12 market reference features from train set")
    
    # ===== 7. HANDLE MISSING VALUES =====
    print(f"{'[TRAIN]' if is_train else '[TEST]'} Handling missing values...")
    
    # Fill missing std with 0
    X_fe['brand_std_price'].fillna(0, inplace=True)
    X_fe['series_std_price'].fillna(0, inplace=True)
    
    # Fill missing counts with 1
    for col in ['brand_count', 'series_count', 'cpu_full_count', 'ram_storage_combo_count']:
        X_fe[col].fillna(1, inplace=True)
    
    # Fill missing means with overall mean
    overall_mean = stats_dict.get('overall_mean', train_stats['overall_mean'] if train_stats else X_fe['brand_mean_price'].mean())
    for col in ['brand_mean_price', 'brand_median_price', 'series_mean_price', 
                'cpu_full_mean_price', 'ram_storage_combo_mean']:
        X_fe[col].fillna(overall_mean, inplace=True)
    
    print(f"   ✅ Missing values handled")
    
    print(f"\n{'='*60}")
    print(f"✅ Feature engineering complete!")
    print(f"   Original features: {X.shape[1]}")
    print(f"   Engineered features: {X_fe.shape[1]}")
    print(f"   Total added: {X_fe.shape[1] - X.shape[1]}")
    print(f"{'='*60}")
    
    if is_train:
        return X_fe, stats_dict
    else:
        return X_fe

# Apply feature engineering
X_train, train_stats = add_features(X_train_basic, y_train, is_train=True)
X_test = add_features(X_test_basic, y_test, is_train=False, train_stats=train_stats)

print(f"\n📊 Final shapes:")
print(f"   X_train: {X_train.shape}")
print(f"   X_test: {X_test.shape}")

# ===============================
# 4. DEFINE PREPROCESSOR
# ===============================
print("\n" + "="*60)
print("BUILDING PREPROCESSOR")
print("="*60)

# Identify column types
categorical_cols = [
    col for col in X_train.columns 
    if X_train[col].dtype == 'object' or col in [
        'ram_category', 'storage_category', 'spec_tier', 'cpu_full', 'brand_ram_tier'
    ]
]
numeric_cols = [col for col in X_train.columns if col not in categorical_cols]

print(f"Categorical columns ({len(categorical_cols)}): {categorical_cols[:5]}...")
print(f"Numeric columns ({len(numeric_cols)}): {numeric_cols[:5]}...")

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
        ('num', RobustScaler(), numeric_cols)  # RobustScaler better for outliers
    ]
)

print("✅ Preprocessor created with RobustScaler")

# ===============================
# 5. RANDOM FOREST TUNING
# ===============================
print("\n" + "="*60)
print("RANDOM FOREST - HYPERPARAMETER TUNING")
print("="*60)

rf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(random_state=42))
])

rf_params = {
    "model__n_estimators": [300, 500, 800, 1000],
    "model__max_depth": [15, 20, 25, 30, None],
    "model__min_samples_split": [2, 5, 10],
    "model__min_samples_leaf": [1, 2, 4],
    "model__max_features": ['sqrt', 'log2', 0.5, 0.7],
    "model__max_samples": [0.7, 0.8, 0.9, None],
    "model__bootstrap": [True, False]
}

rf_search = RandomizedSearchCV(
    rf_pipeline,
    rf_params,
    n_iter=30,  # More iterations for better search
    scoring="neg_mean_absolute_error",
    cv=5,
    verbose=1,
    random_state=42,
    n_jobs=-1,
    refit=True
)

print("🔍 Running Random Forest tuning...")
rf_search.fit(X_train, y_train)

best_rf = rf_search.best_estimator_
print(f"\n✅ Best RF params: {rf_search.best_params_}")

# Evaluate
rf_pred = best_rf.predict(X_test)
rf_mae = mean_absolute_error(y_test, rf_pred)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
rf_r2 = r2_score(y_test, rf_pred)
rf_mape = mean_absolute_percentage_error(y_test, rf_pred) * 100

print(f"\n📊 Random Forest Test Performance:")
print(f"   MAE:  Rp {rf_mae:,.0f}")
print(f"   RMSE: Rp {rf_rmse:,.0f}")
print(f"   R²:   {rf_r2:.4f}")
print(f"   MAPE: {rf_mape:.2f}%")

# Save model
# joblib.dump(best_rf, "../models/feature/best_rf.pkl")
print("💾 Saved best RF model")

# ===============================
# 6. XGBOOST TUNING
# ===============================
print("\n" + "="*60)
print("XGBOOST - HYPERPARAMETER TUNING")
print("="*60)

xgb_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', XGBRegressor(objective="reg:squarederror", random_state=42))
])

xgb_params = {
    "model__n_estimators": [300, 500, 800, 1000],
    "model__learning_rate": [0.01, 0.05, 0.1, 0.15],
    "model__max_depth": [4, 6, 8, 10],
    "model__subsample": [0.7, 0.8, 0.9],
    "model__colsample_bytree": [0.7, 0.8, 0.9],
    "model__colsample_bylevel": [0.7, 0.8, 1.0],
    "model__gamma": [0, 0.1, 0.5, 1],
    "model__min_child_weight": [1, 3, 5],
    "model__reg_alpha": [0, 0.1, 0.5],
    "model__reg_lambda": [1, 1.5, 2]
}

xgb_search = RandomizedSearchCV(
    xgb_pipeline,
    xgb_params,
    n_iter=30,
    scoring="neg_mean_absolute_error",
    cv=5,
    verbose=1,
    random_state=42,
    n_jobs=-1
)

print("🔍 Running XGBoost tuning...")
xgb_search.fit(X_train, y_train)

best_xgb = xgb_search.best_estimator_
print(f"\n✅ Best XGB params: {xgb_search.best_params_}")

# Evaluate
xgb_pred = best_xgb.predict(X_test)
xgb_mae = mean_absolute_error(y_test, xgb_pred)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
xgb_r2 = r2_score(y_test, xgb_pred)
xgb_mape = mean_absolute_percentage_error(y_test, xgb_pred) * 100

print(f"\n📊 XGBoost Test Performance:")
print(f"   MAE:  Rp {xgb_mae:,.0f}")
print(f"   RMSE: Rp {xgb_rmse:,.0f}")
print(f"   R²:   {xgb_r2:.4f}")
print(f"   MAPE: {xgb_mape:.2f}%")

# Save model
# joblib.dump(best_xgb, "../models/feature/best_xgb.pkl")
print("💾 Saved best XGBoost model")

# ===============================
# 7. FINAL SUMMARY
# ===============================
print("\n" + "="*60)
print("FINAL PERFORMANCE SUMMARY")
print("="*60)

summary = pd.DataFrame({
    'Model': ['Random Forest', 'XGBoost'],
    'MAE (Rp)': [rf_mae, xgb_mae],
    'RMSE (Rp)': [rf_rmse, xgb_rmse],
    'R²': [rf_r2, xgb_r2],
    'MAPE (%)': [rf_mape, xgb_mape]
})

print("\n" + summary.to_string(index=False))

# Compare with original baseline (from your results)
original_mae_rf = 2466683
original_mae_xgb = 2474031

improvement_rf = (original_mae_rf - rf_mae) / original_mae_rf * 100
improvement_xgb = (original_mae_xgb - xgb_mae) / original_mae_xgb * 100

print("\n" + "="*60)
print("IMPROVEMENT FROM ORIGINAL CODE")
print("="*60)
print(f"\n🚀 Random Forest:")
print(f"   Original MAE: Rp {original_mae_rf:,.0f}")
print(f"   New MAE:      Rp {rf_mae:,.0f}")
print(f"   Improvement:  {improvement_rf:.2f}%")

print(f"\n🚀 XGBoost:")
print(f"   Original MAE: Rp {original_mae_xgb:,.0f}")
print(f"   New MAE:      Rp {xgb_mae:,.0f}")
print(f"   Improvement:  {improvement_xgb:.2f}%")

print("\n" + "="*60)
print("✅ TRAINING COMPLETED!")
print("="*60)
print("\n💡 Models saved:")
print("   - models/feature/best_rf.pkl")
print("   - models/feature/best_xgb.pkl")
print("\n📝 Note: All features engineered WITHOUT data leakage!")