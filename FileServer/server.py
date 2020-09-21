import os
import zmq
import json

path = "/home/gustavo/files"

#Lee la data del archivo data.json 
def readJson():
    data = {}
    with open(path + "/data.json", "r") as f:
        data = json.load(f)
    
    return data

#Escribe la data en el archivo data.json
def writeJson(data):
    with open(path + "/data.json", "w") as f:
        json.dump(data, f, indent=4)


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
                with open(path + "/" + username + "/" + filename, 'ab') as f:
                    f.write(message[2])
                    socket.send_string(filename + " subido")
            else:            
                with open(path + "/" + username + "/" + filename, 'wb') as f:
                    f.write(message[2])
                    socket.send_string(filename + " subido")
        else:
            print("Hago la carpeta")
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
    elif message[0] == b'verificationUpload':
        hashName = message[1].decode('utf-8')
        filename = message[2].decode('utf-8')
        username = message[3].decode('utf-8')

        data = readJson()
        users = list(data.keys())
        if(username in users):
            if((filename in data[username]['fileName']) and (hashName in data[username]['hashName'])):
                socket.send_multipart('1'.encode('utf-8'))
            elif(not(filename in data[username]['fileName']) and (hashName in data[username]['hashName'])):
                data[username]['fileName'].append(filename)
                writeJson(data)
                socket.send_multipart('2'.encode('utf-8'))
            elif((filename in data[username]['fileName']) and not(hashName in data[username]['hashName'])):
                nombre = filename
                splt = nombre.split(".")
                i = 1
                while nombre in data[username]['fileName']:
                    nombre = splt[0]+'('+str(i)+').'+splt[1]
                    i += 1
                filename = nombre
                data[username]['fileName'].append(nombre)
                data[username]['hashName'].append(hashName)
                writeJson(data)
                socket.send_multipart('3'.encode('utf-8'), filename.encode('utf-8'))


            elif(not(filename in data[username]['fileName']) and not(hashName in data[username]['hashName'])):
                data[username]['fileName'].append(filename)
                data[username]['hashName'].append(hashName)
                writeJson(data)
                socket.send_multipart('4'.encode('utf-8'))
            else:
                print("Error!!")
                socket.send_multipart('Error'.encode('utf-8'))
        else:
            data[username] = {
                'fileName':[],
                'hashName':[]
            }

            data[username]['fileName'].append(filename)
            data[username]['hashName'].append(hashName)
            writeJson(data)
            socket.send_multipart('5'.encode('utf-8'))
    else:
        print("Error!!")        
        socket.send_string("Error")
