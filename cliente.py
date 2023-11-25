import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.0.19"
# host = socket.gethostname() #esta es la dirección ip del servidor.
puerto = 456

msj = input("Msj del cliente: ")

clientsocket.connect((host, puerto))

clientsocket.send(msj.encode("UTF-8"))
print("Datos enviados")

mensaje = clientsocket.recv(1024)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


clientsocket.close()
if mensaje:
    print(mensaje.decode("ascii"))
else:
    print("No se recibieron datos desde el servidor")
