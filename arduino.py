import serial.tools.list_ports


ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

ser = serial.Serial('COM3', baudrate=9600, timeout=2)
print(ser.readlines())
