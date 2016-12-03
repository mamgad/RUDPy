import socket
import sys


#Seq number flag
seqFlag=0


class packet():
    checksum =0;
    length=0;
    seqNo=0;
    msg=0;

    def make(self,data):
        self.msg = data
        self.length = str(len(data)).zfill(3)
        self.seqNo=seqFlag;
        print "Message is %s length is %s seqNo is %s" % (self.msg, self.length, self.seqNo)




sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print  'starting up on %s port %s' % server_address
sock.bind(server_address)
pkt=packet()


while True:
    print  '\nwaiting to receive message'
    data, address = sock.recvfrom(600)

    print  'received %s bytes from %s' % (len(data), address)
    #print  data
    try:
        print 'Opening file %s'%data
        fileRead=open(data , 'r')
        data = fileRead.read()

        fileRead.close()

        #print "content length is data %s" % pkt.length;
        x = 0
        #Fragment and send file 500 byte by 500 byte
        for x in range(0, (len(data) / 500)+1):
            print data[x * 500:x * 500 + 500]
            msg = data[x * 500:x * 500 + 500];
            pkt.make(msg);
            print "length is %s" % str(pkt.length);

            finalPacket = str(pkt.checksum)+","+str(pkt.seqNo)+","+str(pkt.length)+","+pkt.msg

            sent = sock.sendto(finalPacket, address) #send packet
            print  'sent %s bytes back to %s waiting for ack..' % (sent, address)
            ack, address = sock.recvfrom(100);
            print(ack)
            x = +1
            
        #fileRead.close();


    except:#fail opening file
        print "error opening file"
        exit()

