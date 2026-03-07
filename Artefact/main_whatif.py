import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load real collected data

file_name = "drought_data.csv"
data = pd.read_csv(file_name)

data.columns = data.columns.str.strip()

cols = ["temp", "moisture", "moisture_factor", "temp_factor", "drought_prob"]
for col in cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna()


def drought_prob_calc(temp, moisture):
    """Recalculate drought probability from raw sensor values."""
    moisture_factor = 1 - moisture / 1023
    temp_factor = temp / 40
    return 0.65 * moisture_factor + 0.35 * temp_factor


def risk_level(x):
    if x > 0.7:
        return "High"
    elif x > 0.5:
        return "Medium"
    else:
        return "Low"


'''
What-If Scenario 1: Temperature Increase
Simulates a heatwave — what if temperatures
rose by +5C and +10C across all readings?
'''

scenario1 = data.copy()
scenario1["drought_prob_plus5"] = scenario1.apply(
    lambda row: drought_prob_calc(row["temp"] + 5, row["moisture"]), axis=1
)
scenario1["drought_prob_plus10"] = scenario1.apply(
    lambda row: drought_prob_calc(row["temp"] + 10, row["moisture"]), axis=1
)

'''
What-If Scenario 2: Critically Dry Soil
Simulates a drought — what if soil moisture
dropped to 200 (very dry) across all readings?
'''

scenario2 = data.copy()
scenario2["drought_prob_dry"] = scenario2.apply(
    lambda row: drought_prob_calc(row["temp"], 200), axis=1
)
scenario2["drought_prob_very_dry"] = scenario2.apply(
    lambda row: drought_prob_calc(row["temp"], 50), axis=1
)

'''
What-If Scenario 3: Combined Worst Case
What if both temp rose +8C AND soil was
critically dry, eg. moisture = ~100?
'''

scenario3 = data.copy()
scenario3["drought_prob_worst"] = scenario3.apply(
    lambda row: drought_prob_calc(row["temp"] + 8, 100), axis=1
)
scenario3["drought_prob_best"] = scenario3.apply(
    lambda row: drought_prob_calc(row["temp"] - 3, 900), axis=1
)

'''
Prit Summary Results
'''

print("=" * 55)
print("  WHAT-IF SCENARIO ANALYSIS — DROUGHT PREDICTION")
print("=" * 55)

print("\n--- Scenario 1: Temperature Heatwave ---")
print(f"  Baseline avg drought risk:      {data['drought_prob'].mean():.3f}  ({risk_level(data['drought_prob'].mean())})")
print(f"  +5C avg drought risk:           {scenario1['drought_prob_plus5'].mean():.3f}  ({risk_level(scenario1['drought_prob_plus5'].mean())})")
print(f"  +10C avg drought risk:          {scenario1['drought_prob_plus10'].mean():.3f}  ({risk_level(scenario1['drought_prob_plus10'].mean())})")

print("\n--- Scenario 2: Soil Dryness ---")
print(f"  Baseline avg drought risk:      {data['drought_prob'].mean():.3f}  ({risk_level(data['drought_prob'].mean())})")
print(f"  Dry soil (200) avg risk:        {scenario2['drought_prob_dry'].mean():.3f}  ({risk_level(scenario2['drought_prob_dry'].mean())})")
print(f"  Very dry soil (50) avg risk:    {scenario2['drought_prob_very_dry'].mean():.3f}  ({risk_level(scenario2['drought_prob_very_dry'].mean())})")

print("\n--- Scenario 3: Combined Worst vs Best Case ---")
print(f"  Worst case (+8C, moisture=100): {scenario3['drought_prob_worst'].mean():.3f}  ({risk_level(scenario3['drought_prob_worst'].mean())})")
print(f"  Best case  (-3C, moisture=900): {scenario3['drought_prob_best'].mean():.3f}  ({risk_level(scenario3['drought_prob_best'].mean())})")
print("=" * 55)

'''
Visualise All Scenarios
'''

plt.style.use("seaborn-v0_8-pastel")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("What-If Scenario Analysis — Drought Prediction System", fontsize=14, fontweight="bold")

reading_index = range(len(data))

# Scenario 1 Plot
axes[0].plot(reading_index, data["drought_prob"],       label="Baseline",  color="steelblue",  linewidth=2)
axes[0].plot(reading_index, scenario1["drought_prob_plus5"],  label="+5C",   color="orange",     linewidth=1.5, linestyle="--")
axes[0].plot(reading_index, scenario1["drought_prob_plus10"], label="+10C",  color="red",        linewidth=1.5, linestyle=":")
axes[0].axhline(0.7, color="red",    linestyle="--", alpha=0.4, label="High threshold")
axes[0].axhline(0.5, color="orange", linestyle="--", alpha=0.4, label="Medium threshold")
axes[0].set_title("Scenario 1: Heatwave Effect")
axes[0].set_xlabel("Reading Number")
axes[0].set_ylabel("Drought Probability")
axes[0].legend(fontsize=8)
axes[0].set_ylim(0, 1)

# Scenario 2 Plot
axes[1].plot(reading_index, data["drought_prob"],             label="Baseline",         color="steelblue", linewidth=2)
axes[1].plot(reading_index, scenario2["drought_prob_dry"],      label="Dry soil (200)",   color="sandybrown", linewidth=1.5, linestyle="--")
axes[1].plot(reading_index, scenario2["drought_prob_very_dry"], label="Very dry soil (50)", color="sienna", linewidth=1.5, linestyle=":")
axes[1].axhline(0.7, color="red",    linestyle="--", alpha=0.4, label="High threshold")
axes[1].axhline(0.5, color="orange", linestyle="--", alpha=0.4, label="Medium threshold")
axes[1].set_title("Scenario 2: Soil Dryness Effect")
axes[1].set_xlabel("Reading Number")
axes[1].set_ylabel("Drought Probability")
axes[1].legend(fontsize=8)
axes[1].set_ylim(0, 1)

# Scenario 3 Plot
categories = ["Best Case\n(-3C, moist=900)", "Baseline", "Worst Case\n(+8C, moist=100)"]
averages   = [
    scenario3["drought_prob_best"].mean(),
    data["drought_prob"].mean(),
    scenario3["drought_prob_worst"].mean()
]
bar_colors = ["mediumseagreen", "steelblue", "tomato"]
bars = axes[2].bar(categories, averages, color=bar_colors, edgecolor="white", width=0.5)
axes[2].axhline(0.7, color="red",    linestyle="--", alpha=0.5, label="High threshold")
axes[2].axhline(0.5, color="orange", linestyle="--", alpha=0.5, label="Medium threshold")
for bar, val in zip(bars, averages):
    axes[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                 f"{val:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
axes[2].set_title("Scenario 3: Best vs Worst Case")
axes[2].set_ylabel("Average Drought Probability")
axes[2].set_ylim(0, 1)
axes[2].legend(fontsize=8)

plt.tight_layout()
plt.savefig("whatif_scenarios.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nGraph saved as 'whatif_scenarios.png'")