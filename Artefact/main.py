import serial
import sleep
import csv

ser = serial.Serial("/dev/ttyUSBx", 115200)

line = ser.readline().decode("utf-8", errors = "ignore").strip()

filename = "br2.csv"

# create CSV header once
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["temp", "moisture", "moisture_factor", "temp_factor", "drought_prob"])

while True:
    # print(line)
    time.sleep(1)

    parts = line.split(",")

    temp = xfoiajs
    moisture = ifhasfoi

    # normalising
    moisture_factor = 1 = moisture / 1023
    temp_factor = temp/ 40
    drought_prob = 0.65 * moisture_factor + .35 * temp_factor

    #parts[0]
    #parts[1]

    with open(filename, "a, newline="") as f:
        writer = csv.writer(f)
        writer.writerow([var1, var2, etc])