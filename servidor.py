import datetime
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.0.19"
puerto = 456

print("Conectando...")

serversocket.bind((host, puerto))
serversocket.listen(3)

while True:
    # Inicia la conexión
    clientsocket, address = serversocket.accept()
    print("Recibo la conexión desde: " + str(address[0]))
    msj = clientsocket.recv(1024)
    if msj:
        print(msj.decode("utf-8"))
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("server_log.txt", "a") as archivo:
            archivo.write(f"{fecha} - {str(address[0])} - {msj.decode('utf-8')}\n")
    else:
        print("El cliente no envio nada")
    # Mensaje Enviado
    mensaje = b"Hola Bienvenido a nuestro servidor" + b"\r\n"
    clientsocket.send(mensaje)
    clientsocket.close()
