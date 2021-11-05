#
# A simple UDP Ethernet script to read incoming
# packets from the microcontroller and log them
# in output/out.txt.
#
# To run this: "sudo python3 Ethernet_Comm.py"
#
# Note that sudo is required since this creates a socket
# on the Ethernet port.
#
import socket, datetime

# Start the server socket (ss).
print("Starting server socket...")
ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.bind(("169.254.108.19", 37))
print("UDP Server Up and Listening")

# Open the output file.
outfile = open("output/out.txt", 'a')

while True:
    # Read an incoming packet.
    msg,addr = ss.recvfrom(1024)
    # Create the timestamp.
    d = datetime.datetime.now().strftime("[%m/%d/%Y %H:%M:%S.%f] ")
    # Decode the data.
    data = msg.decode()
    # Filter out miscellaneous characters that may exist at the end of the packet.
    data = data[:len(data)-1]
    # Split on '\n' to get different sensor data points.
    data_arr = data.split('\n')
    # Log each data point.
    for data_point in data_arr:
        outfile.write(d + data_point + '\n')
