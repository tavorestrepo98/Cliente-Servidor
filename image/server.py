import time
import zmq

context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Socket Created!!")

while True:
    message = socket.recv()
    with open("/home/gustavo/rick.jpg", "wb") as f:
        f.write(message)

    socket.send_string("Ok")