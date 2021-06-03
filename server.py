import socket
import ssl.ServerSsl as ServerSsl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1338))
s.listen(5)

while True:
    client, addr = s.accept()
    print("Connected: ", addr[0])

    server = ServerSsl.ServerSsl()
    print( server.sslCommunication(client) ) #key and vector to decryption and encryption

