import socket
import hashlib

# Delimiter
delimiter = "|:|:|";

# Start - Connection initiation
while 1:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 10000)
    userInput = raw_input("\nRequested file: \n")
    message = userInput;
    seqNoFlag = 0
    f = open("r_" + userInput, 'w');

    try:
        # Send data
        print  'Requesting %s' % message
        sent = sock.sendto(message, server_address)
        # Receive indefinitely
        while 1:
            # Receive response
            print  '\nWaiting to receive..'
            data, server = sock.recvfrom(4096)
            seqNo = data.split(delimiter)[1]
            print "Server hash: " + data.split(delimiter)[0]
            print "Client hash: " + hashlib.md5(data.split(delimiter)[3]).hexdigest()[:8]
            if data.split(delimiter)[0] == hashlib.md5(data.split(delimiter)[3]).hexdigest()[:8] and seqNoFlag == int(seqNo == True):
                packetLength = data.split(delimiter)[2]
                f.write(data.split(delimiter)[3]);
                print "Sequence number: %s\nLength: %s" % (seqNo, packetLength);
                print "Server: %s on port %s" % server;
                sent = sock.sendto(str(seqNo) + "," + packetLength, server)
            else:
                print "Checksum mismatch detected, dropping packet"
                print "Server: %s on port %s" % server;
                continue;
            if int(packetLength) < 500:
                seqNo = int(not seqNo)
                break

    finally:
        print "Closing socket"
        sock.close()
        f.close()