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
        cert = open("ssl/certs/cert1.pem", "rb")

        client.sendall( cert.read() + b'.\r\n\r\n' ) #server send cert
        data = self.waitForData(client, b'\r\n\r\n') #server wait for encrypted symmetric key and vector
    
        privateKeyFile = open("ssl/keys/skey.pem", "rb")
        
        private_key = serialization.load_pem_private_key(
            privateKeyFile.read(),
            password=b"123"
        )

        try:
            message = RsaEncryption.decrypt( private_key, data[:-4] ) #server use private key to decrypt message
            
            if( message == False ):
                client.sendall(b'400 failed to decrypt bad encrypted data\r\n\r\n')
                return False 

            elif( self.validCode(message) ):
                message = message.split(b'\r\n')

                if len(message) < 2 :
                    raise ValueError()

                self.clientKey = message[0][4:]
                self.clientVector = message[1]

                if ( len(self.clientKey) not in [16, 24, 32] 
                     #or len(self.clientVector) not in [16, 24, 32] 
                ):
                    client.sendall(b'400 bad key length\r\n\r\n')
                    return False 

                client.sendall(b'200 symetric key decryption done\r\n\r\n')
                return True
            else:
                client.sendall(b'400 response code not valid\r\n\r\n')
        except ValueError:
            client.sendall(b"400 symetric key decryption error\r\n\r\n") 
        return False





    
    







