import socket
import sys
import threading


# Seq number flag
seqFlag=0

# Packet class definition
class packet():
    checksum=0;
    length=0;
    seqNo=0;
    msg=0;
    def make(self,data):
        self.msg = data
        self.length = str(len(data))
        print "Message: %s\nLength: %s\nSequence number: %s" % (self.msg, self.length, self.seqNo)

# Connection handler
def handleConnection(address,data):
    threadSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    thread_server_address = ('localhost', 10001)
    threadSock.bind(thread_server_address)
    try:
        # Read requested file
        print 'Opening file %s' % data
        fileRead=open(data , 'r')
        data = fileRead.read()
        fileRead.close()
                
        # Fragment and send file 500 byte by 500 byte
        x = 0
        for x in range(0, (len(data) / 500) + 1):
            msg = data[x * 500:x * 500 + 500];
            pkt.make(msg);
            finalPacket = str(pkt.checksum)+","+str(pkt.seqNo)+","+str(pkt.length)+","+pkt.msg
            
            # Send packet
            sent = threadSock.sendto(finalPacket, address) 
            print  'Sent %s bytes back to %s, awaiting acknowledgment..' % (sent, address)
            ack, address = threadSock.recvfrom(100);
            if (ack.split(",")[0]==str(pkt.seqNo)):
                pkt.seqNo=(pkt.seqNo+1)%2
            print("Acknowledgment: " + ack)
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
pkt=packet()

# Listening for requests indefinitely
while True:
    print  '\nWaiting to receive message'
    data, address = sock.recvfrom(600)
    connectionThread = threading.Thread(target=handleConnection, args=(address, data))
    connectionThread.start()
    print  'Received %s bytes from %s' % (len(data), address)