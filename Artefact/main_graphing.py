import pandas as pd
import matplotlib.pyplot as plt

# Load Data 

file_name = "drought_data.csv"

data = pd.read_csv(file_name)

print("Data successfully loaded!")


# Basic Cleaning 

data.columns = data.columns.str.strip()

# ensure numeric
cols = ["temp", "moisture", "moisture_factor", "temp_factor", "drought_prob"]
for col in cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna()


# analysis 

print("\n--- Analysis Summary ---")

avg_temp = data["temp"].mean()
avg_moisture = data["moisture"].mean()
avg_risk = data["drought_prob"].mean()

print(f"Average Temperature: {avg_temp:.2f} °C")
print(f"Average Soil Moisture: {avg_moisture:.2f}")
print(f"Average Drought Risk: {avg_risk:.2f}")


# dedect drought levels
def risk_level(x):
    if x > 0.7:
        return "High"
    elif x > 0.5:
        return "Medium"
    else:
        return "Low"

data["risk_level"] = data["drought_prob"].apply(risk_level)


# Visualising 

plt.style.use("seaborn-v0_8-pastel")
plt.figure(figsize=(18,5))


# Temperature over time
plt.subplot(1,3,1)

plt.plot(data["temp"], color="red")
plt.title("Temperature Readings")
plt.xlabel("Reading Number")
plt.ylabel("Temperature (°C)")


# Moisture vs Temperature
plt.subplot(1,3,2)

plt.scatter(data["moisture"], data["temp"], color="blue")
plt.title("Moisture vs Temperature")
plt.xlabel("Moisture")
plt.ylabel("Temperature")


# Drought Risk Distribution
plt.subplot(1,3,3)

risk_counts = data["risk_level"].value_counts()

plt.pie(
    risk_counts,
    labels=risk_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Drought Risk Levels")

plt.tight_layout()
plt.show()


print("\nFirst 5 Rows:")
print(data.head())