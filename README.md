# Week 1 — Strategic Planning and Data Exploration in Logistics

## Project overview
This repository contains the Week 1 strategic plan for a Python-based logistics analytics project focused on shipment reliability and logistics cost.

## Objectives
- Define logistics KPIs.
- Plan data collection, cleaning, EDA, and model evaluation.
- Provide starter Python code for KPI calculation.
- Document public research sources and project limitations.

## Files
- `Week1_Logistics_Strategic_Planning_Report.docx` — report for submission.
- `src/logistics_kpi_analysis.py` — starter KPI analysis script.
- `requirements.txt` — Python dependencies.
- `data/` — place the downloaded dataset here. The raw dataset is not included in this repository.
- `outputs/` — generated KPI outputs.

## Dataset
Candidate source: DataCo SMART Supply Chain for Big Data Analysis  
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

Review the dataset licence and data dictionary before use. Map the source columns to the normalized column names expected by the script. Do not commit personal, confidential, or restricted data.

## Setup on Windows (VS Code / PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, either run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the current terminal and activate again, or use the environment interpreter directly:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\logistics_kpi_analysis.py
```

Put your normalized CSV at `data/shipments.csv`, then run:
```powershell
python src\logistics_kpi_analysis.py
```

Expected columns: `order_id`, `order_date`, `promised_delivery_date`, `actual_delivery_date`, `shipping_mode`, `region`, `shipping_cost`. The script is a template and needs a column mapping if your dataset uses different field names.

## Research links
- World Bank LPI data: https://datacatalog.worldbank.org/search/dataset/0038649/logistics-performance-index
- World Bank LPI 2.0 methodology: https://lpi.worldbank.org/en/about/methodology
- pandas documentation: https://pandas.pydata.org/docs/user_guide/index.html
- scikit-learn model selection: https://scikit-learn.org/stable/model_selection.html

## Status
Planning and starter code only. Do not report performance findings or business savings until the dataset has been analyzed and the results validated.
