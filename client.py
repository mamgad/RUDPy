import socket
import sys




# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)

userInput=raw_input("File to be requested:")
message=userInput;
try:

    # Send data
    print  'sending "%s"' % message
    sent = sock.sendto(message, server_address)

    # Receive response
    print  'waiting to receive'
    data, server = sock.recvfrom(4096)
    print  'received "%s"' % data



    sent = sock.sendto("ack -------", server_address)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()