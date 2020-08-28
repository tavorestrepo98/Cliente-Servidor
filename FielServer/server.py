import os
import zmq

def filesName():
    contenido = os.listdir("/home/gustavo/files")
    listado = []
    for l in contenido:
        listado.append(l.encode('utf-8')) 

    return listado


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

        #buscamos los nombres que hay en la carpeta
        content = os.listdir("/home/gustavo/files")

        #si el nombre existe, cambio el nombre
        if(filename in content):
            filename2 = filename
            parts = filename.split('.')
            i = 1
            while(filename2 in content):
                filename2 = parts[0]+"("+str(i)+")."+parts[1]
                i = i+1

            with open('/home/gustavo/files/'+filename2, 'wb') as f:
                f.write(message[2])
                socket.send_string(filename2)

        else:            
            with open('/home/gustavo/files/'+filename, 'wb') as f:
                f.write(message[2])
                socket.send_string(filename)

    elif message[0] == b'list':
        names = filesName()      
        socket.send_multipart(names)

    elif message[0] == b'download':
        filename = message[1].decode('utf-8')

        content = os.listdir("/home/gustavo/files")

        if(filename in content):        
            with open('/home/gustavo/files/'+filename, 'rb') as f:
                socket.send_multipart(['ok'.encode('utf-8'), f.read()])
                print("download")
                #socket.send_multipart[['Error!'.encode('utf-8')]]
        else:
            socket.send_multipart(['Error!'.encode('utf-8'), 'El archivo no se encuentra'.encode('utf-8')])
    else:
        print("Error!!")        
        socket.send_string("Error")
