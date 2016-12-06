import socket
import threading
import hashlib
import time
import datetime

# Seq number flag
seqFlag = 0

# Packet class definition
class packet():
    checksum = 0;
    length = 0;
    seqNo = 0;
    msg = 0;

    def make(self, data):
        self.msg = data
        self.length = str(len(data))
        self.checksum=hashlib.md5(data).hexdigest()[:8]
        print "Length: %s\nSequence number: %s" % (self.length, self.seqNo)


# Connection handler
def handleConnection(address, data):
    start_time=time.time()
    print "Request started at: " + str(datetime.datetime.utcnow())
    pkt = packet()
    threadSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Read requested file
        print "Opening file %s" % data
        fileRead = open(data, 'r')
        data = fileRead.read()
        fileRead.close()

        # Fragment and send file 500 byte by 500 byte
        x = 0
        while x < (len(data) / 500) + 1:
            msg = data[x * 500:x * 500 + 500];
            pkt.make(msg);
            finalPacket = str(pkt.checksum) + "|:|:|" + str(pkt.seqNo) + "|:|:|" + str(pkt.length) + "|:|:|" + pkt.msg

            # Send packet
            sent = threadSock.sendto(finalPacket, address)
            print  'Sent %s bytes back to %s, awaiting acknowledgment..' % (sent, address)
            threadSock.settimeout(2)
            try:
                ack, address = threadSock.recvfrom(100);
            except:
                print "Time out reached, resending ...%s" % x;
                continue;
            if ack.split(",")[0] == str(pkt.seqNo):
                pkt.seqNo = int(not pkt.seqNo)
                print "Acknowledged by: " + ack + "\nAcknowledged at: " + str(datetime.datetime.utcnow()) + "\nElapsed: " + str(time.time()-start_time)
                x += 1

    # File opening failure handling
    except:
        print "Error on opening the requested file"


# Start - Connection initiation
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print  'Starting up on %s port %s' % server_address
sock.bind(server_address)

# Listening for requests indefinitely
while True:
    print  'Waiting to receive message'
    data, address = sock.recvfrom(600)
    connectionThread = threading.Thread(target=handleConnection, args=(address, data))
    connectionThread.start()
    print  'Received %s bytes from %s' % (len(data), address)
