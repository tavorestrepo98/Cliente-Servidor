import time
import zmq

context = zmq.Context()

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

with open("/home/gustavo/pepino.jpg", "rb") as f:
    bytesImage = f.read()
    socket.send(bytesImage)

    resp = socket.recv_string()
    print(resp)




