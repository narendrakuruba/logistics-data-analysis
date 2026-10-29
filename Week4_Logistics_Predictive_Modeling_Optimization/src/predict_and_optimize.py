"""
Week 4: Predictive Modeling and Optimization in Logistics Systems
Dataset: hypothetical_logistics_shipments.csv (synthetic demonstration data).
Run from the project root:
    pip install -r requirements.txt
    python src/predict_and_optimize.py
"""
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hypothetical_logistics_shipments.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["shipment_date"]).sort_values("shipment_date")
target = "delivery_hours"
features = [
    "distance_km", "weight_kg", "transport_mode", "weather",
    "traffic_index", "region", "priority", "holiday_period"
]
X, y = df[features], df[target]

numeric = ["distance_km", "weight_kg", "traffic_index", "holiday_period"]
categorical = ["transport_mode", "weather", "region", "priority"]
preprocess = ColumnTransformer([
    ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), numeric),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ]), categorical)
])

# Keep the newest 20% as a holdout test set to imitate forecasting future shipments.
split = int(len(df) * 0.80)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42, max_depth=8),
    "Random Forest": RandomForestRegressor(
        n_estimators=180, random_state=42, min_samples_leaf=3, n_jobs=-1
    )
}
rows = []
fitted = {}
for name, model in models.items():
    pipe = Pipeline([("prep", preprocess), ("model", model)])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    rows.append({
        "model": name,
        "MAE_hours": mean_absolute_error(y_test, pred),
        "RMSE_hours": mean_squared_error(y_test, pred) ** 0.5,
        "R2": r2_score(y_test, pred)
    })
    fitted[name] = pipe

# Tune Random Forest with time-series cross-validation on training data only.
rf_pipe = Pipeline([
    ("prep", preprocess),
    ("model", RandomForestRegressor(random_state=42, n_jobs=-1))
])
param_grid = {
    "model__n_estimators": [100, 180],
    "model__max_depth": [None, 12],
    "model__min_samples_leaf": [2, 4]
}
cv = TimeSeriesSplit(n_splits=4)
search = GridSearchCV(
    rf_pipe, param_grid, scoring="neg_mean_absolute_error",
    cv=cv, n_jobs=-1, refit=True
)
search.fit(X_train, y_train)
tuned_pred = search.best_estimator_.predict(X_test)
rows.append({
    "model": "Tuned Random Forest",
    "MAE_hours": mean_absolute_error(y_test, tuned_pred),
    "RMSE_hours": mean_squared_error(y_test, tuned_pred) ** 0.5,
    "R2": r2_score(y_test, tuned_pred)
})
metrics = pd.DataFrame(rows).sort_values("MAE_hours")
metrics.to_csv(OUT / "model_evaluation_metrics.csv", index=False)
print("Model evaluation (newest 20% held out):")
print(metrics.to_string(index=False))
print("\\nBest tuning parameters:", search.best_params_)

# Save predictions from tuned model for operational review.
predictions = X_test.copy()
predictions["actual_delivery_hours"] = y_test.values
predictions["predicted_delivery_hours"] = tuned_pred.round(2)
predictions["prediction_error_hours"] = (
    predictions["actual_delivery_hours"] - predictions["predicted_delivery_hours"]
).round(2)
predictions.to_csv(OUT / "test_set_predictions.csv", index=False)

# Simple decision-support scenario: estimate effect of reducing road traffic index by 1.
scenario = X_test.copy()
scenario["traffic_index"] = np.maximum(1, scenario["traffic_index"] - 1)
baseline_pred = search.best_estimator_.predict(X_test)
scenario_pred = search.best_estimator_.predict(scenario)
impact = pd.DataFrame({
    "baseline_predicted_hours": baseline_pred,
    "scenario_predicted_hours": scenario_pred,
})
impact["estimated_hours_saved"] = impact["baseline_predicted_hours"] - impact["scenario_predicted_hours"]
impact.to_csv(OUT / "traffic_reduction_scenario.csv", index=False)
print("\\nIllustrative scenario: reduce traffic index by one point")
print("Average predicted hours saved per shipment:",
      round(impact["estimated_hours_saved"].mean(), 2))
print("Note: this is a model-based scenario, not proof of a causal effect.")
