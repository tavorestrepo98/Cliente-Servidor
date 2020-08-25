import time
import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

#  Wait for next request from client
while(True):
    message = socket.recv_string()
    print("operation is server: %s" % message)

    num1 = message[0]
    op = message[1]
    num2 = message[2]

    result = 0

    if(op == '+'):
        result = int(num1) + int(num2)
    elif(op == '-'):
        result = int(num1) - int(num2)
    elif(op == '*'):
        result = int(num1) * int(num2)
    elif((op == '/') and (int(num2) != 0) ):
        result = int(num1) / int(num2)

    time.sleep(2)

    #  Send result of operation
    socket.send_string(str(result))