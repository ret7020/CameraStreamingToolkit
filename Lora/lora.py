import serial


ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.flushInput()
# Setting temp data(until reboot)
# Address
#ser.write(b'\xC0\x00\x02\xFF\xFF')
# Getting data
ser.write(b'\xC1\x00\x02')
r_data = ser.read(5)
print(r_data)

#ser.flushInput()

#ser.write(b'\xC1\x00\x02')
#r_data = ser.read(5)
#print("Address registers", r_data)

#ser.write(b"\x12\x12\x12\xAA")
while 1:
    r_data = ser.read(4)
    print(r_data)



