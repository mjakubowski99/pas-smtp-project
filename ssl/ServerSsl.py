import socket
import ssl.encryption.RsaEncryption as RsaEncryption
from cryptography.hazmat.primitives import serialization

supported_algos_symetric = [ 
    'aes-256-ecb'
]

supported_algos_asymetric = [
    'rsa-2048'
]

class ServerSsl:
    def __init__(self):
        self.clientKey = b''
        self.errorMessage = b''

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

    def verifyAlgorithm(self, algos):
        if( len(algos) < 3):
            self.errorMessage = b'401 Bad format'
            return False 

        if( algos[0] != 'support'):
            self.errorMessage = b'401 Bad format'
            return False 

        supported_asymetric = False
        for supp_algo in supported_algos_asymetric:
            if algos[1] == 'asymetric-'+supp_algo:
                supported_asymetric=True
 
        if not supported_asymetric:
            self.errorMessage = b'502 not supported asymetric algorithm'

        supported_symetric = False
        for supp_algo in supported_algos_symetric:
            if algos[2] == 'symetric-'+supp_algo+'?':
                supported_symetric = True

        if not supported_symetric:
            self.errorMessage = b'502 not supported symetric algorithm'

        return supported_symetric and supported_asymetric #check if both algorithms are valid


    def sslCommunication(self, client):
        hello = self.waitForData(client, b'\r\n\r\n').decode('utf-8')

        if( hello[:-4] != 'hello ssl1.0?'  ):
            client.sendall(b'503 not supported ssl version\r\n\r\n')
            return False
        else:
            client.sendall(b'201 ssl valid\r\n\r\n')

        message= self.waitForData(client, b'\r\n\r\n').decode('utf-8')  
        algos = message[:-4].split(' ')

        if( not self.verifyAlgorithm(algos) ):
            client.sendall(self.errorMessage+b".\r\n\r\n")
            return False 
        
        cert = open("ssl/certs/cert1.pem", "rb")

        client.sendall( b"202 algos valid" + cert.read() + b'.\r\n\r\n' ) #server send cert
        data = self.waitForData(client, b'\r\n\r\n') #server wait for encrypted symmetric key and vector
    
        privateKeyFile = open("ssl/keys/skey.pem", "rb")
        
        private_key = serialization.load_pem_private_key(
            privateKeyFile.read(),
            password=b"123"
        )

        try:
            message = RsaEncryption.decrypt( private_key, data[:-4] ) #server use private key to decrypt message
            
            if( message == False ):
                client.sendall(b'504 symetric key decryption error\r\n\r\n')
                return False 

            else:
                self.clientKey = message

                if ( len(self.clientKey) not in [16, 24, 32] 
                     #or len(self.clientVector) not in [16, 24, 32] 
                ):
                    client.sendall(b'505 bad client key length\r\n\r\n')
                    return False 

                client.sendall(b'203 symetric key decryption done\r\n\r\n')
                return True
        except ValueError:
            client.sendall(b"504 symetric key decryption error\r\n\r\n") 
        return False





    
    







