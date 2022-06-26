import serial
import csv

#Serial port outputs all cell voltages contiguously (e.g. 300003100035000...29000\r\n)
#see image for clarification

NUM_Data = 4     #number of data points per row
Data_len = 5     #length of each data point

serialPort = serial.Serial(port="COM4", baudrate=115200, bytesize=8, timeout=10, stopbits=serial.STOPBITS_ONE)

serialString = ""  # Used to hold data coming over UART
count = 0

logFile = "data.csv"        #File for data to be written into

with open(logFile, 'w', newline='') as dataFile:        
    dataWriter = csv.writer(dataFile)
    
    #first line of data (header for data)
    dataWriter.writerow(["time (ms)", "Cell 1", "Cell 2", "Cell 3", "Cell 4"])

while 1:
    if serialPort.in_waiting > 0:
        cells=[]
        cells=[0 for i in range(NUM_Data)]

        for i in range(NUM_Data):
            rawData = serialPort.read(Data_len)            
            cells[i] = rawData.decode('Ascii')
        endBits1 = serialPort.read(2)
        if(endBits1 == b'\r\n'):
            with open(logFile, 'a', newline='') as dataFile:
                dataWriter = csv.writer(dataFile)
                dataWriter.writerow([str(count), str(cells[0]), str(cells[1]), str(cells[2]), str(cells[3])])
        count = count + 0.1
