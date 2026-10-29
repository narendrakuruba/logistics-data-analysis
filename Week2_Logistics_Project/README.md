# Week 2 — Data Collection, Cleaning, and Preprocessing for Logistics Analysis

This project documents a reproducible preprocessing workflow for logistics shipment data.

## Contents
- `Week2_Logistics_Data_Cleaning_Preprocessing_Report.docx` — report for submission.
- `src/preprocess_logistics.py` — starter preprocessing script.
- `requirements.txt` — Python dependencies.
- `data/` — local dataset folder; raw data is not included.
- `outputs/` — generated quality profile, outlier review, and cleaned CSV.

## Candidate dataset
DataCo SMART Supply Chain for Big Data Analysis:
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

Check the current dataset licence, terms, and data dictionary before downloading. Do not commit personal, confidential, or restricted data.

## Windows setup
Open this folder in VS Code and run in PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the current terminal, or call `.\.venv\Scripts\python.exe` directly.

Place your permitted CSV at `data/shipments_raw.csv`, inspect its columns, and map source fields as needed. Then run:
```powershell
python src\preprocess_logistics.py
```

The script profiles missingness, removes exact duplicate rows only, parses known date/numeric fields when present, trims text whitespace, flags IQR outliers for review, and saves outputs. It does not blindly impute critical fields or automatically delete outliers.

Existing Week 1 repository: https://github.com/narendrakuruba/logistics-data-analysis
