import serial
import csv
import codecs
import time

serialPort = serial.Serial(port="COM11", baudrate=9600, bytesize=8, timeout=10, stopbits=serial.STOPBITS_ONE)

serialString = ""  # Used to hold data coming over UART
count = 0

with open('data.csv', 'w', newline='') as dataFile:
    dataWriter = csv.writer(dataFile)
    dataWriter.writerow(["time (ms)", "X-Axis Acc (G)", "Y-Axis Acc (G)", "Z-Axis Acc (G)", "ADC (mV)", "CAN ID", "CAN Data"])
    start = time.time()

while 1:
    if serialPort.in_waiting > 0:
        # Read data out of the buffer until a carraige return / new line is found
        serialStringX = serialPort.read(2)
        serialStringY = serialPort.read(2)
        serialStringZ = serialPort.read(2)
        serialStringADC = serialPort.read(2)
        CANID = serialPort.read(1)
        CANData = serialPort.read(1)
        nowGx = (int.from_bytes(serialStringX, byteorder='big', signed=True) / 16384) - 0.192
        nowGy = (int.from_bytes(serialStringY, byteorder='big', signed=True) / 16384) - 0.178
        nowGz = (int.from_bytes(serialStringZ, byteorder='big', signed=True) / 16384) - 0.096
        nowADC = int.from_bytes(serialStringADC, byteorder='big', signed=True) / 1.218
        CANID = codecs.encode(CANID, "hex")
        CANData = codecs.encode(CANData, "hex")
        count = count + 0.01
        with open('data.csv', 'a', newline='') as dataFile:
            dataWriter = csv.writer(dataFile)
            dataWriter.writerow([str(count), str(nowGx), str(nowGy), str(nowGz), str(nowADC), str(CANID), str(CANData)])
            print(count)
            if count > 10:
                end = time.time()
                print("Time:", end - start)
                break
