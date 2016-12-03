import socket
import sys

# Start - Connection initiation
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)
userInput=raw_input("Requested file: ")
message=userInput;
f = open("rec "+userInput, 'a');

try:
    # Send data
    print  'Requesting %s' % message
    sent = sock.sendto(message, server_address)
    # Receive indefinitely
    while(1):
    # Receive response
        print  'Waiting to receive..'
        data, server = sock.recvfrom(4096)
        print  'Received: %s' % data
        seqNo = data.split(",")[1]
        packetLength = data.split(",")[2]
        print "Message content: %s" % data.split(",")[3]
        f.write(data.split(",")[3]);

        print "Sequence number: %s\nLength: %s" % (seqNo, packetLength);
        print "Server: %s\nPort: %s" % server;
        sent = sock.sendto(str(seqNo) + "," + packetLength, server)


finally:
    print >> sys.stderr, 'Closing socket'
    sock.close()
    f.close()