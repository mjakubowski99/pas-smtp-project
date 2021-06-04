import socket
import os 

from cryptography import x509
import ssl.encryption.CertificateVerification as CertificateVerification
import ssl.encryption.SymetricEncryption as Encryption
import ssl.encryption.RsaEncryption as RsaEncryption

class ClientSsl:
    def __init__(self, sock, rootCert):
        self.sock = sock
        self.rootCert = rootCert.read()
        self.certData = None 

    def waitForData(self):
        data = b''
        while b'\r\n\r\n' not in data:
            data += self.sock.recv(1) 
        return data 

    def verifyCert(self):
        data = self.waitForData()
        if CertificateVerification.verifyCertificate( data[:-4], self.rootCert ):
            self.certData = data[:-2]
            print("Trusted cert")
            return True
        else:
            print("Not trusted cert")
            self.sock.close()
            return False

    def getPublicKey(self):
        return x509.load_pem_x509_certificate(self.certData).public_key()

    def genSymetricKey(self):
        self.key = os.urandom(32)
        self.vector = os.urandom(16)

    def getEncryptedSymetricKey(self):
        toEncrypt = b"200 " + self.key + b'\r\n' + self.vector

        return RsaEncryption.encrypt(
            self.getPublicKey(),
            toEncrypt
        )

    def sslCommunication(self):
        if( not self.verifyCert() ):
            return 

        self.genSymetricKey()
        key = self.getEncryptedSymetricKey()
        
        self.sock.sendall( key+b'\r\n\r\n' )
        data = self.waitForData()
        print(data)

        


        
            
        