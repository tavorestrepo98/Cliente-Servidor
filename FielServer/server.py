import os
import zmq

path = "/home/gustavo/files"


def filesName(username):
    contenido = os.listdir(path + "/" + username)
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
        username = message[3].decode('utf-8')
        #buscamos los nombres que hay en la carpeta
        content = os.listdir(path)

        #verificamos que sí está el username
        if(username in content):
            content2 = os.listdir(path + "/" + username)
            #si el nombre existe, cambio el nombre
            if(filename in content2):
                socket.send_string("El archivo ya existe, por favor cambie el nombre")
            else:            
                with open(path + "/" + username + "/" + filename, 'wb') as f:
                    f.write(message[2])
                    socket.send_string(filename + " subido")
        else:
            os.mkdir(path + "/" + username)
            with open(path + "/" + username + "/" + filename, 'wb') as f:
                    f.write(message[2])
                    socket.send_string(filename + " subido")

            

    elif message[0] == b'list':
        username = message[1].decode('utf-8')

        content = os.listdir(path)

        if(username in content):
            names = filesName(username)      
            socket.send_multipart(names)
        else: 
            socket.send_multipart(["Error".encode('utf-8')])        

    elif message[0] == b'download':
        filename = message[1].decode('utf-8')
        username = message[2].decode('utf-8')

        content = os.listdir(path)

        #Si está la carpeta del usuario
        if(username in content):
            content2 = os.listdir(path + "/" + username)

            #if para verificar si el archivo existe en el servidor
            if(filename in content2):        
                with open(path + "/" + username + "/" +filename, 'rb') as f:
                    socket.send_multipart(['ok'.encode('utf-8'), f.read()])
                    print("download")
            else:
                socket.send_multipart(["Error!".encode('utf-8'), "El archivo no se encuentra en la carpeta del usuario ".encode('utf-8')])
        else:
            socket.send_multipart(["Error2!".encode('utf-8'), "No existe el usuario ".encode('utf-8')])
    else:
        print("Error!!")        
        socket.send_string("Error")
