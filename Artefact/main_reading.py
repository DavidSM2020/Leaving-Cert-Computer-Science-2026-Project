import serial
import time
import csv

# connect to microbit
ser = serial.Serial("COM3", 115200)

filename = "drought_data.csv"

# create CSV header
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["temp", "moisture", "moisture_factor", "temp_factor", "drought_prob"])

print("Started logging")

while True:

    line = ser.readline().decode("utf-8", errors="ignore").strip()

    if line == "":
        continue

    print("Raw:", line)   # shows exactly what the microbit sent

    try:
        parts = line.split(",")

        temp = float(parts[0])
        moisture = float(parts[1])

        # normalising
        moisture_factor = 1 - moisture / 1023
        temp_factor = temp / 40

        drought_prob = 0.65 * moisture_factor + 0.35 * temp_factor

        print(f"Temp: {temp} | Moisture: {moisture} | Risk: {drought_prob:.2f}")

        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([temp, moisture, moisture_factor, temp_factor, drought_prob])

    except Exception as e:
        print("Error:", e)

    time.sleep(1)