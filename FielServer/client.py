import zmq
import sys

context = zmq.Context()

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")
cmd = sys.argv[1]

if cmd == 'upload':
    #Subir el archivo
    filename = sys.argv[2]
    print("subiendo {}".format(filename))
    with open("/home/gustavo/"+filename, 'rb') as f:
        bytes = f.read()
        socket.send_multipart([b"upload", filename.encode('utf-8'), bytes])
        resp = socket.recv_string()
        print(resp)

elif cmd == 'list':
    print("Listar!!!")
    socket.send_multipart([b"list"])
    lista = socket.recv_multipart()

    #Valido si la lista de archivos está vacía
    if(lista == []):
        print("La carpeta está vacía")
    else:
        for i in lista:
            print(i.decode('utf-8'))

elif cmd == 'download':
    filename = sys.argv[2]
    socket.send_multipart([b"download", filename.encode('utf-8')])

    resp = socket.recv_multipart()
    if(resp[0].decode('utf-8') == 'ok'):
        downFile = resp[1]
        with open('/home/gustavo/FilesDownload/'+filename, 'wb') as f:
            f.write(resp[1])
            print('{} download'.format(filename))

else:
    print("Error!")