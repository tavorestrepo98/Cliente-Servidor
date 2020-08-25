import zmq
import sys

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

op = sys.argv[1]
print(op)

socket.send_string(op)

#  Get the reply.
message = socket.recv_string()
print("the result of operation is: %s" % message)