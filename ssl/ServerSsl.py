import socket
import ssl.encryption.RsaEncryption as RsaEncryption
from cryptography.hazmat.primitives import serialization

class ServerSsl:
    def __init__(self):
        self.clientKey = b''
        self.clientVector = b''

    def waitForData(self, client, byteEnd):
        data = b''
        while byteEnd not in data:
            data += client.recv(1) 
        return data

    def validCode(self, message):
        try:
            return message[0:4].decode('utf-8') == "200 "
        except Exception:
            return False 

    def sslCommunication(self, client):
        cert = open("ssl/certs/serverCert.pem", "rb")
        client.sendall( cert.read() + b'\r\n' )
        data = self.waitForData(client, b'\r\n\r\n')
    
        privateKeyFile = open("ssl/certs/key.pem", "rb")
        private_key = serialization.load_pem_private_key(
            privateKeyFile.read(),
            password=b"pass123"
        )
        try:
            message = RsaEncryption.decrypt( private_key, data[:-4] )
            if( self.validCode(message) ):
                message = message.split(b'\r\n')
                self.clientKey = message[0]
                self.clientVector = message[1]

                client.sendall(b'200 symetric key decryption done\r\n')
                return (self.clientKey, self.clientVector)
            else:
                client.sendall(b'400 response code not valid\r\n')
        except Exception:
            client.sendall(b'400 symetric key decryption error\r\n') 
        return ()





    
    







