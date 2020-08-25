import os
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
        filename = message[1].decode('utf-8')
        print(filename + " Upload")

        with open('/home/gustavo/files/'+filename, 'wb') as f:
            f.write(message[2])
        socket.send_string("Listo!! "+filename+" subido")
    elif message[0] == b'list':
        contenido = os.listdir("/home/gustavo/files")
        print(contenido)
        listado = []
        for l in contenido:
            listado.append(l.encode('utf-8'))

        socket.send_multipart(listado)
    elif message[0] == b'download':
        filename = message[1].decode('utf-8')
        
        with open('/home/gustavo/files/'+filename, 'rb') as f:
            socket.send_multipart(['ok'.encode('utf-8'), f.read()])
            print("download")
            #socket.send_multipart[['Error!'.encode('utf-8')]]
    else:
        print("Error!!")
        socket.send_string("Error")
