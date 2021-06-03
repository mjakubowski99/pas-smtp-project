import socket
import ssl.ClientSsl as ClientSsl 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect( ('127.0.0.1', 1338) )

    client = ClientSsl.ClientSsl(s, open("ssl/certs/cert.pem", "rb") )
    client.sslCommunication()
except socket.error:
    print("Socket error")