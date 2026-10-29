# Week 4 — Predictive Modeling and Optimization in Logistics Systems

## Project objective
Forecast shipment delivery time (hours) from shipment distance, weight, transport mode, weather, traffic, region, priority, and holiday period. Compare baseline models and tune a Random Forest model, then use predictions to support operational scenarios.

## Dataset
`data/hypothetical_logistics_shipments.csv` contains 1,200 synthetic shipment records. It is generated for learning and does not represent real company performance.

## Project structure
- `data/`: synthetic shipment dataset
- `src/predict_and_optimize.py`: complete model training, evaluation, tuning, and scenario analysis
- `outputs/model_evaluation_metrics.csv`: model comparison metrics
- `outputs/test_set_predictions.csv`: held-out predictions and errors
- `outputs/traffic_reduction_scenario.csv`: illustrative traffic scenario
- `outputs/*.png`: visualizations
- `Week4_Predictive_Modeling_Optimization_Report.docx`: detailed report

## Run on Windows
Open PowerShell in this folder and run:
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe src\predict_and_optimize.py
```
Using `.venv\Scripts\python.exe` avoids PowerShell activation-policy issues.

## Method
Chronological 80/20 split; compare Linear Regression, Decision Tree, Random Forest, and tuned Random Forest. The newest 20% is held out as a test set. Hyperparameters are selected using 4-fold `TimeSeriesSplit` cross-validation on training data only. Metrics: MAE, RMSE, and R².

## Important limitation
All records are simulated. Results are demonstration results only. Validate on representative real operational data, check drift and fairness, and do not automate dispatch decisions without human review.
