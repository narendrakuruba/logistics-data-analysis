from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "shipments_raw.csv"
OUTPUT = ROOT / "outputs"
OUTPUT.mkdir(exist_ok=True)

df_raw = pd.read_csv(INPUT)
df = df_raw.copy()

# Standardize headers to lowercase snake_case
df.columns = (
    df.columns.astype(str).str.strip().str.lower()
      .str.replace(r"[^a-z0-9]+", "_", regex=True)
      .str.strip("_")
)

# Initial quality profile
profile = pd.DataFrame({
    "dtype": df.dtypes.astype(str),
    "missing_count": df.isna().sum(),
    "missing_pct": (df.isna().mean() * 100).round(2),
    "unique_values": df.nunique(dropna=True),
})
profile.to_csv(OUTPUT / "data_quality_profile.csv")
print("Raw shape:", df_raw.shape)
print("Exact duplicate rows:", int(df.duplicated().sum()))

# Remove exact duplicate rows only; repeated IDs may be valid
df = df.drop_duplicates().copy()

# Map these names to actual source columns as needed
date_cols = ["order_date", "ship_date",
             "promised_delivery_date", "actual_delivery_date"]
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

numeric_cols = ["shipping_cost", "sales", "quantity", "weight"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Standardize whitespace in text fields
for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].astype("string").str.strip()

# Flag IQR outliers for investigation; do not auto-delete
outlier_summary = []
for col in numeric_cols:
    if col in df.columns:
        s = df[col].dropna()
        if not s.empty:
            q1, q3 = s.quantile([0.25, 0.75])
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            flag = df[col].lt(lower) | df[col].gt(upper)
            outlier_summary.append({
                "column": col, "lower_bound": lower,
                "upper_bound": upper, "flagged_count": int(flag.sum())
            })
pd.DataFrame(outlier_summary).to_csv(
    OUTPUT / "outlier_review.csv", index=False
)

# Example chronology flag
if {"order_date", "ship_date"}.issubset(df.columns):
    df["order_after_ship_flag"] = df["order_date"] > df["ship_date"]

# Do not blindly impute critical dates, IDs, or outcome labels.
df.to_csv(OUTPUT / "shipments_cleaned.csv", index=False)
print("Cleaned shape:", df.shape)
print("Outputs saved to:", OUTPUT)
