# My ML Course

Early machine learning coursework — data preprocessing and regression modeling, worked through mostly in Jupyter notebooks with scikit-learn.

## Structure

- **`Preprocessing data/`** — handling missing values, encoding, feature scaling, train/test splits.
- **`Regression/`** — one folder per technique, each with its own dataset and exercise notebook:
  - `simple-linear-regression/`
  - `multiple-linear-regression/`
  - `polynomial-regression/`
  - `decision-tree-regression/`
  - `random-forest-regression/`
  - `support-vector-regresion/`
  - `best-model-selection/` — comparing all of the above on the same dataset to pick a winner.
- **`Beta Testing Hackathon DQLab/`** — two timed hackathon exercises (data cleaning/standardization, and market-basket analysis with the Apriori algorithm).

## Stack

`streamlit`, `pandas`, `numpy`, `scikit-learn`, `xgboost`, `joblib` — see `requirements.txt`.

## Status

This track is complete; the active project has moved on to [`../ai-engineer/`](../ai-engineer) — an LLM/RAG-focused build (Veritas) — using what was learned here as the ML foundation.
