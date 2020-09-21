import zmq
import sys
import hashlib
import json


context = zmq.Context()

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

def uploadFile(filename, username, partsize):
    print("Subir el archivo desde una función")
    with open("/home/gustavo/"+filename, 'rb') as f:
        myBytes = 0
        while myBytes:
            myBytes = f.read(partsize)
            socket.send_multipart([b"upload", filename.encode('utf-8'), myBytes, username.encode('utf-8')])
            resp = socket.recv_string()
            print("Respuesta: " + resp)
    print("Done!!!")

cmd = sys.argv[1]

if cmd == 'upload':
    #Subir el archivo
    filename = sys.argv[2]
    username = sys.argv[3]
    print("subiendo {}".format(filename))
    partsize = 1024*100 #100kb

    hasher = hashlib.md5()
    with open("/home/gustavo/"+filename, 'rb') as f:
        bytes = f.read()
        hasher.update(bytes)

    hashName = hasher.hexdigest()
    print(hashName)

    #verificamos primero si el archivo ya existe y tiene el mismo nombre
    socket.send_multipart([b'verificationUpload',hashName.encode('utf-8'), filename.encode('utf-8'), username.encode('utf-8')])
    respu = socket.recv_multipart()
    valid = respu[0].decode('utf-8')
    print(valid)

    if(valid == '1'):
        print("El archivo ya existe!")
    elif(valid == '2'):
        print("Subir")
        with open("/home/gustavo/"+filename, 'rb') as f:
            while bytes:
                bytes = f.read(partsize)
                socket.send_multipart([b"upload", filename.encode('utf-8'), bytes, username.encode('utf-8')])
                resp = socket.recv_string()
                print("Respuesta: " + resp)
        print("Done!!!")
    elif(valid == '3'):
        filename = respu[1].decode('utf-8')
        print("Subir")
        with open("/home/gustavo/"+filename, 'rb') as f:
            while bytes:
                bytes = f.read(partsize)
                socket.send_multipart([b"upload", filename.encode('utf-8'), bytes, username.encode('utf-8')])
                resp = socket.recv_string()
                print("Respuesta: " + resp)
        print("Done!!!")
    elif(valid == '4'):
        print("Subir")
        with open("/home/gustavo/"+filename, 'rb') as f:
            while bytes:
                bytes = f.read(partsize)
                socket.send_multipart([b"upload", filename.encode('utf-8'), bytes, username.encode('utf-8')])
                resp = socket.recv_string()
                print("Respuesta: " + resp)
        print("Done!!!")
    elif(valid == '5'):
        print("Subir")
        with open("/home/gustavo/"+filename, 'rb') as f:
            while bytes:
                bytes = f.read(partsize)
                socket.send_multipart([b"upload", filename.encode('utf-8'), bytes, username.encode('utf-8')])
                resp = socket.recv_string()
                print("Respuesta: " + resp)
        print("Done!!!")

    elif(valid == 'Error'):
        print('Error!')

    """ with open("/home/gustavo/"+filename, 'rb') as f:
        while bytes:
            bytes = f.read(partsize)
            socket.send_multipart([b"upload", filename.encode('utf-8'), bytes, username.encode('utf-8')])
            resp = socket.recv_string()
            print("Respuesta: " + resp)
    print("Done!!!") """

elif cmd == 'list':
    username = sys.argv[2]
    print("Listar!!!")
    socket.send_multipart([b"list", username.encode('utf-8')])
    resp = socket.recv_multipart()

    #Valido si la lista de archivos está vacía
    if(resp[0] == b"Error"):
        print("El usuario no ha subido archivos aún")
    else:
        for i in resp:
            print(i.decode('utf-8'))

elif cmd == 'download':
    filename = sys.argv[2]
    username = sys.argv[3]

    socket.send_multipart([b"download", filename.encode('utf-8'), username.encode('utf-8')])
    resp = socket.recv_multipart()
    if(resp[0].decode('utf-8') == 'ok'):
        downFile = resp[1]
        with open('/home/gustavo/FilesDownload/'+filename, 'wb') as f:
            f.write(resp[1])
            print('{} download'.format(filename))
    elif(resp[0].decode('utf-8') == "Error!"):
        print(resp[1].decode('utf-8')+username) 
    elif(resp[0].decode('utf-8') == "Error2!"):
        print(resp[1].decode('utf-8')+username) 
    else:
        print("Ha ocurrido un error!")

else:
    print("Error!")