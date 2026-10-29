from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "shipments.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

REQUIRED = [
    "order_id", "order_date", "promised_delivery_date",
    "actual_delivery_date", "shipping_mode", "region", "shipping_cost"
]

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Download a permitted public dataset, map its columns to the expected schema, "
            "and save it as data/shipments.csv."
        )

    df = pd.read_csv(DATA_PATH)
    missing_cols = [c for c in REQUIRED if c not in df.columns]
    if missing_cols:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing_cols) +
            "\nAvailable columns: " + ", ".join(map(str, df.columns)) +
            "\nCreate a documented column mapping before running the analysis."
        )

    for col in ["order_date", "promised_delivery_date", "actual_delivery_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["shipping_cost"] = pd.to_numeric(df["shipping_cost"], errors="coerce")

    print("Shape:", df.shape)
    print("\nMissing values (%):")
    print((df.isna().mean().mul(100).round(1)).sort_values(ascending=False))
    print("\nExact duplicate rows:", int(df.duplicated().sum()))

    valid = df.dropna(subset=["promised_delivery_date", "actual_delivery_date"]).copy()
    valid["is_late"] = valid["actual_delivery_date"] > valid["promised_delivery_date"]
    valid["delivery_lead_days"] = (
        valid["actual_delivery_date"] - valid["order_date"]
    ).dt.total_seconds() / 86400

    summary = pd.DataFrame([{
        "shipments_with_valid_dates": len(valid),
        "on_time_rate_pct": round((~valid["is_late"]).mean() * 100, 2),
        "late_rate_pct": round(valid["is_late"].mean() * 100, 2),
        "average_lead_days": round(valid["delivery_lead_days"].mean(), 2),
        "average_shipping_cost": round(df["shipping_cost"].mean(), 2),
    }])
    summary.to_csv(OUTPUT_DIR / "overall_kpis.csv", index=False)

    by_mode = (
        valid.groupby("shipping_mode", dropna=False)
        .agg(
            shipment_rows=("order_id", "size"),
            unique_orders=("order_id", "nunique"),
            late_rate_pct=("is_late", lambda s: round(s.mean() * 100, 2)),
            average_lead_days=("delivery_lead_days", "mean"),
            average_shipping_cost=("shipping_cost", "mean"),
        )
        .reset_index()
    )
    by_mode.to_csv(OUTPUT_DIR / "kpis_by_shipping_mode.csv", index=False)
    print("\nOverall KPIs\n", summary.to_string(index=False))
    print("\nKPIs by shipping mode\n", by_mode.to_string(index=False))
    print(f"\nSaved outputs in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
