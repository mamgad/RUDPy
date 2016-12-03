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
    while(1):
    # Receive response
        print  'waiting to receive'
        data, server = sock.recvfrom(4096)

        print  'received "%s"' % data
        seqNo = data.split(",")[1]
        packetLength = data.split(",")[2]
        print "seqNo = %s len is %s" % (seqNo, packetLength);
        print server;
        sent = sock.sendto(str(seqNo) + "," + packetLength, server)


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()