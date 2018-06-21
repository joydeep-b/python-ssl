import socket
import struct
import sys
import protogen.proto.referee_pb2 as referee_pb2

multicast_group = '224.5.23.1'
server_address = ('', 10003)

# multicast_group = '224.3.29.71'
# server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Receive/respond loop
ref_msg = referee_pb2.SSL_Referee()
while True:
    # print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(1024)
    ref_msg.ParseFromString(data)
    print '%d: %s' % (ref_msg.packet_timestamp,
            ref_msg.command)
    print referee_pb2._SSL_REFEREE_COMMAND.values_by_number[ref_msg.command].name
    # print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    # print >>sys.stderr, data

    # print >>sys.stderr, 'sending acknowledgement to', address
    sock.sendto('ack', address)
