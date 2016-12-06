import socket
import threading
import hashlib
import time
import datetime
import random
import sys

# Delimiter
delimiter = "|:|:|";

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
    drop_count=0
    packet_count=0
    time.sleep(0.5)
    packet_loss_percentage=float(raw_input("Enter a packet loss percentage (0-100): \n"))/100.0
    while packet_loss_percentage<0 or packet_loss_percentage >= 1:
        packet_loss_percentage = float(raw_input("Enter a packet loss percentage (0-99): \n"))/100.0
    start_time=time.time()
    print "Request started at: " + str(datetime.datetime.utcnow())
    pkt = packet()
    threadSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Read requested file

        try:
            print "Opening file %s" % data
            fileRead = open(data, 'r')
            data = fileRead.read()
            fileRead.close()
        except:
            print "error opening requested file"
            msg="FNF";
            pkt.make(msg);
            finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter + pkt.msg
            threadSock.sendto(finalPacket, address)
            return 0 ;


        # Fragment and send file 500 byte by 500 byte
        x = 0
        while x < (len(data) / 500) + 1:
            packet_count += 1
            randomised_plp = random.random()
            if packet_loss_percentage < randomised_plp:
                msg = data[x * 500:x * 500 + 500];
                pkt.make(msg);
                finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(
                    pkt.length) + delimiter + pkt.msg

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
                    print "Acknowledged by: " + ack + "\nAcknowledged at: " + str(
                        datetime.datetime.utcnow()) + "\nElapsed: " + str(time.time() - start_time)
                    x += 1
            else:
                print "\n------------------------------\n\t\tDropped packet\n------------------------------\n"
                drop_count += 1
        print "Packets: " + str(packet_count) + "\nDropped packets: " + str(drop_count)+"\nComputed drop rate: %.2f" % float(float(drop_count)/float(packet_count)*100.0)
    except:
        print " "



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