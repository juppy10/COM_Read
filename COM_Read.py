import serial
import csv
import codecs
import time

def gpgll_parse(sentence):
    words = sentence.split(',')
    if words[1] != '':
        nmealat = words[1].split('.')
        lat = int(nmealat[0][:-2]) + int(nmealat[0][-2:]) / 60 + int(nmealat[1]) / (60 * pow(10, len(nmealat[1])))
        if words[2] == 'S':
            lat = -lat

        nmealon = words[3].split('.')
        lon = int(nmealon[0][:-2]) + int(nmealon[0][-2:]) / 60 + int(nmealon[1]) / (60 * pow(10, len(nmealon[1])))
        if words[4] == 'W':
            lon = -lon

        return lat, lon
    return 0, 0

serialPort = serial.Serial(port="COM11", baudrate=9600, bytesize=8, timeout=10, stopbits=serial.STOPBITS_ONE)

serialString = ""  # Used to hold data coming over UART
count = 0

with open('data.csv', 'w', newline='') as dataFile:
    dataWriter = csv.writer(dataFile)
    dataWriter.writerow(["time (ms)", "X-Axis Acc (G)", "Y-Axis Acc (G)", "Z-Axis Acc (G)", "ADC (mV)", "CAN ID", "CAN Data", "GNSS Data (lat)", "GNSS Data (lon)"])
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
        GNSS_Length = int.from_bytes(serialPort.read(1), byteorder='big')
        GNSS_Data = serialPort.read(GNSS_Length)
        nowGx = (int.from_bytes(serialStringX, byteorder='big', signed=True) / 16384) - 0.14
        nowGy = (int.from_bytes(serialStringY, byteorder='big', signed=True) / 16384) - 0.17
        nowGz = (int.from_bytes(serialStringZ, byteorder='big', signed=True) / 16384) - 0.099
        nowADC = int.from_bytes(serialStringADC, byteorder='big', signed=True) / 1.218
        CANID = codecs.encode(CANID, "hex")
        CANData = codecs.encode(CANData, "hex")
        GNSS_Data = GNSS_Data.decode('Ascii')
        count = count + 0.01
        [lat, lon] = gpgll_parse(GNSS_Data)
        with open('data.csv', 'a', newline='') as dataFile:
            dataWriter = csv.writer(dataFile)
            dataWriter.writerow([str(count), str(nowGx), str(nowGy), str(nowGz), str(nowADC), str(CANID), str(CANData), lat, lon])
            print(count)
            if count > 10:
                end = time.time()
                print("Time:", end - start)
                break
