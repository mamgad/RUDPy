import socket
import hashlib
import os

# Set address and port
serverAddress = "localhost"
serverPort = 10000

# Delimiter
delimiter = "|:|:|";

# Start - Connection initiation
while 1:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(10);
    server_address = (serverAddress, serverPort)
    userInput = raw_input("\nRequested file: ")
    message = userInput;
    seqNoFlag = 0
    f = open("r_" + userInput, 'w');

    try:
        # Connection trials
        connection_trials_count=0
        # Send data
        print  'Requesting %s' % message
        sent = sock.sendto(message, server_address)
        # Receive indefinitely
        while 1:
            # Receive response
            print  '\nWaiting to receive..'
            try:
                data, server = sock.recvfrom(4096)
                # Reset failed trials on successful transmission
                connection_trials_count=0;
            except:
                connection_trials_count += 1
                if connection_trials_count < 5:
                    print "\nConnection time out, retrying"
                    continue
                else:
                    print "\nMaximum connection trials reached, skipping request\n"
                    os.remove("r_" + userInput)
                    break
            seqNo = data.split(delimiter)[1]
            clientHash = hashlib.sha1(data.split(delimiter)[3]).hexdigest()
            print "Server hash: " + data.split(delimiter)[0]
            print "Client hash: " + clientHash
            if data.split(delimiter)[0] == clientHash and seqNoFlag == int(seqNo == True):
                packetLength = data.split(delimiter)[2]
                if data.split(delimiter)[3] == "FNF":
                    print ("Requested file could not be found on the server")
                    os.remove("r_" + userInput)
                else:
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