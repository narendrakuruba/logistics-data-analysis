# Week 3: Advanced Data Analysis and Visualization in Logistics

This project demonstrates EDA on a **hypothetical, synthetic dataset** of 300 shipments. It does not represent real company performance.

## Dataset
Includes region, transport mode, distance, shipment volume, weather, delivery time, transportation cost, and delivery status.

## Setup (Windows PowerShell)
```powershell
python -m pip install -r requirements.txt
python src/analyze_logistics.py
```
The script prints quality checks, descriptive statistics, correlations, and grouped summaries, and saves charts to `outputs/`.

Tools: Python, Pandas, NumPy, Matplotlib. All records are simulated for learning.
