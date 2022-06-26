# COM_Read

Tool used by myself during my thesis as a COM Port data logging tool. 

A flexible (if you can be bothered to change it) tool to gather data from COM port to a CSV. 

## Usage
First edit the script for the correct COM port, baud rate, size, etc.
```python
serialPort = serial.Serial(port="COM4", baudrate=115200, bytesize=8, timeout=10, stopbits=serial.STOPBITS_ONE)
```
Then set the correct log file,
```python
logFile = "data.csv"        #File for data to be written into
```

Set the correct data length and size (this could be implemented better, idc).
```python
NUM_Data = 4     #number of data points per row
Data_len = 5     #length of each data point
```
The tool will log each line of data as a row (i.e. each row must be finished with a "\r\n")