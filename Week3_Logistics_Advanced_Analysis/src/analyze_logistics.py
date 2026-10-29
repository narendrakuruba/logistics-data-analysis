from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data"/"hypothetical_logistics_dataset.csv")
out=ROOT/"outputs"; out.mkdir(exist_ok=True)
num=["distance_km","shipment_volume_units","delivery_time_hours","transportation_cost_usd"]
print("Shape:",df.shape)
print("Missing values:\n",df.isna().sum())
print("Duplicate rows:",df.duplicated().sum())
print("Descriptive statistics:\n",df[num].describe().round(2))
print("Correlations:\n",df[num].corr().round(3))
print("By transport mode:\n",df.groupby("transport_mode").agg(shipments=("shipment_id","count"),avg_cost=("transportation_cost_usd","mean"),avg_hours=("delivery_time_hours","mean"),late_rate=("delivery_status",lambda s:(s=="Late").mean()*100)).round(2))
plt.figure(figsize=(8,5)); plt.hist(df.delivery_time_hours,bins=20,edgecolor="black"); plt.title("Distribution of Delivery Times"); plt.xlabel("Hours"); plt.ylabel("Shipments"); plt.tight_layout(); plt.savefig(out/"delivery_time_distribution.png",dpi=150); plt.close()
df.groupby("transport_mode").transportation_cost_usd.mean().sort_values().plot(kind="bar",title="Average Transportation Cost by Mode"); plt.xlabel("Mode"); plt.ylabel("Cost (USD)"); plt.tight_layout(); plt.savefig(out/"average_cost_by_mode.png",dpi=150); plt.close()
plt.figure(figsize=(8,5))
for mode,g in df.groupby("transport_mode"): plt.scatter(g.distance_km,g.transportation_cost_usd,label=mode,alpha=.65)
plt.title("Distance and Transportation Cost"); plt.xlabel("Distance (km)"); plt.ylabel("Cost (USD)"); plt.legend(); plt.tight_layout(); plt.savefig(out/"distance_vs_cost.png",dpi=150); plt.close()
corr=df[num].corr(); plt.figure(figsize=(7,5)); plt.imshow(corr,vmin=-1,vmax=1,cmap="coolwarm"); plt.xticks(range(4),["Distance","Volume","Delivery hours","Cost"],rotation=20,ha="right"); plt.yticks(range(4),["Distance","Volume","Delivery hours","Cost"])
for i in range(4):
 for j in range(4): plt.text(j,i,f"{corr.iloc[i,j]:.2f}",ha="center",va="center")
plt.colorbar(); plt.title("Correlation Matrix"); plt.tight_layout(); plt.savefig(out/"correlation_heatmap.png",dpi=150); plt.close()
df.groupby("weather_condition").delivery_time_hours.mean().reindex(["Normal","Rain","Severe"]).plot(kind="bar",title="Average Delivery Time by Weather"); plt.xlabel("Weather"); plt.ylabel("Hours"); plt.tight_layout(); plt.savefig(out/"delivery_time_by_weather.png",dpi=150); plt.close()
(df.assign(is_late=df.delivery_status.eq("Late")).groupby("region").is_late.mean()*100).sort_values(ascending=False).plot(kind="bar",title="Late Delivery Rate by Region"); plt.xlabel("Region"); plt.ylabel("Late deliveries (%)"); plt.tight_layout(); plt.savefig(out/"late_rate_by_region.png",dpi=150); plt.close()
print("Charts saved in",out)
