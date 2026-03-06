import serial

ser = serial.Serial("COM3", 115200)

print("Listening...")

while True:
    line = ser.readline()
    print(line)