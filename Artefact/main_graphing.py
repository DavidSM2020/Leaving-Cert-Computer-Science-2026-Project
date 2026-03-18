import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load Data
file_name = "drought_data.csv"
data = pd.read_csv(file_name)
print("Data successfully loaded!")

# Basic Cleaning
data.columns = data.columns.str.strip()

cols = ["temp", "moisture", "moisture_factor", "temp_factor", "drought_prob"]
for col in cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna()
data = data.reset_index(drop=True)

# Analysis
print("\n--- Analysis Summary ---")

avg_temp     = data["temp"].mean()
avg_moisture = data["moisture"].mean()
avg_risk     = data["drought_prob"].mean()
max_temp     = data["temp"].max()
min_moisture = data["moisture"].min()

print(f"Average Temperature:    {avg_temp:.2f} °C")
print(f"Max Temperature:        {max_temp:.2f} °C")
print(f"Average Soil Moisture:  {avg_moisture:.2f}")
print(f"Min Soil Moisture:      {min_moisture:.2f}")
print(f"Average Drought Risk:   {avg_risk:.2f}")

# Detect drought risk levels
def risk_level(x):
    if x > 0.7:
        return "High"
    elif x > 0.5:
        return "Medium"
    else:
        return "Low"

data["risk_level"] = data["drought_prob"].apply(risk_level)

risk_counts = data["risk_level"].value_counts()
print(f"\nRisk Level Breakdown:")
for level, count in risk_counts.items():
    print(f"  {level}: {count} readings ({count / len(data) * 100:.1f}%)")

# Visualising
plt.style.use("seaborn-v0_8-pastel")
fig = plt.figure(figsize=(18, 5))
fig.suptitle("Drought Prediction System — Data Analysis", fontsize=14, fontweight="bold")

# Temperature over time with trend line
plt.subplot(1, 3, 1)

plt.plot(data["temp"], color="red", linewidth=1.5, label="Temperature", alpha=0.7)

if len(data) >= 10:
    trend = data["temp"].rolling(window=10, center=True).mean()
    plt.plot(trend, color="darkred", linewidth=2, linestyle="--", label="Trend (10-pt avg)")

plt.title("Temperature Readings")
plt.xlabel("Reading Number")
plt.ylabel("Temperature (°C)")
plt.legend(fontsize=9)

# Moisture vs Temperature scatter, colour coded by drought risk
plt.subplot(1, 3, 2)

scatter = plt.scatter(
    data["moisture"],
    data["temp"],
    c=data["drought_prob"],
    cmap="RdYlGn_r",
    edgecolors="white",
    linewidths=0.3,
    alpha=0.85
)
plt.colorbar(scatter, label="Drought Probability")
plt.title("Moisture vs Temperature")
plt.xlabel("Moisture (raw sensor value)")
plt.ylabel("Temperature (°C)")

# Drought Risk Distribution pie chart
plt.subplot(1, 3, 3)

all_levels = ["High", "Medium", "Low"]
risk_counts_full = risk_counts.reindex(all_levels, fill_value=0)
colors = ["tomato", "orange", "mediumseagreen"]

plt.pie(
    risk_counts_full,
    labels=risk_counts_full.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors
)
plt.title("Drought Risk Levels")

plt.tight_layout()
plt.savefig("analysis_graphs.png", dpi=150, bbox_inches="tight")
plt.show()

print("\nFirst 5 Rows:")
print(data.head())
print("\nGraph saved as 'analysis_graphs.png'")
