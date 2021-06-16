
import socket
import os 

from cryptography import x509
import ssl.encryption.CertificateVerification as CertificateVerification
import ssl.encryption.SymetricEncryption as Encryption
import ssl.encryption.RsaEncryption as RsaEncryption
from cryptography.hazmat.primitives import serialization

class ClientSsl:
    def __init__(self, sock, caPublicKey):
        self.sock = sock
        self.caPublicKey = caPublicKey.read()
        self.certData = None 

    def waitForCert(self):
        data = b''
        while b'.\r\n\r\n' not in data:
            data += self.sock.recv(1) 
        return data 

    def waitForData(self):
        data = b''
        while b'\r\n\r\n' not in data:
            data += self.sock.recv(1) 
        return data 

    def algorithmsValid(self, data):
        return data.decode('utf-8').startswith('202 algos valid')

    def verifyCert(self):
        data = self.waitForCert()

        if( not self.algorithmsValid(data) ):
            print("Server not support one of this algorithms: ")
            print("Server message: ", data.decode('utf-8') )
            return False

        if( len(data) < 7 ):
            print("It's sure that certificate is not valid")
            return False 
        
        if CertificateVerification.verifyCertificate( data[15:-5], self.caPublicKey ):
            self.certData = data[15:-5]
            print("Trusted cert")
            return True
        else:
            print("Not trusted cert")
            self.sock.close()
            return False

    def getPublicKey(self):
        cert = x509.load_pem_x509_certificate(self.certData)
        return cert.public_key()

    def genSymetricKey(self):
        self.key = os.urandom(32)
    
    def codeValid(self, data):
        return data.decode('utf-8').startswith('203 ')

    def getEncryptedSymetricKey(self):
        toEncrypt = self.key

        encryptedData = RsaEncryption.encrypt(
                self.getPublicKey(),
                toEncrypt
            )

        try:
            encryptedData = RsaEncryption.encrypt(
                self.getPublicKey(),
                toEncrypt
            )
            return encryptedData
        except ValueError:
            return False 

    def sslCommunication(self):
        self.sock.sendall(b'hello ssl1.0?\r\n\r\n')

        data = self.waitForData()
        if( data.decode('utf-8')[:-4] != "201 ssl valid"):
            print("Server not support this ssl protocol version")
            return False

        print("Server support ssl 1.0")
        self.sock.sendall(b'support asymetric-rsa-2048 symetric-aes-256-ecb?\r\n\r\n')

        if( not self.verifyCert() ): #receive and verify certificate
            return False

        print("Server support asymetric-rsa-2048 symetric-aes-256-ecb")

        self.genSymetricKey() #gen symetric key
        key = self.getEncryptedSymetricKey() #encrypt keys with server public key

        if( key != False ): #if encryption successfull
            self.sock.sendall( key+b'\r\n\r\n' ) #send encrypted keys to server
            data = self.waitForData() #wait for server response

            return self.codeValid(data)
        else:
            return False


        

        


        
            
        