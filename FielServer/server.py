import zmq

context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Socket created!!")

files = []

## 1. Upload a file
## 2. download a file
## 3. list files

while True:
    message = socket.recv_multipart()
    if message[0] == b'upload':
        #Client wants to upload a file