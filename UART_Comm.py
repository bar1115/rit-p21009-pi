import serial, datetime

outfile = open("output/out.txt", 'a')
serialport = serial.Serial("COM8", baudrate=576000, timeout=0.1)

while True:
    rcv = serialport.read_until(size=256)
    if (rcv):
        d = datetime.datetime.now().strftime("[%m/%d/%Y %H:%M:%S.%f] ")
        outfile.write(d + rcv.strip().decode() + '\n')
