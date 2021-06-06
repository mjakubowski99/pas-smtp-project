
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

    def verifyCert(self):
        data = self.waitForCert()
        if CertificateVerification.verifyCertificate( data[:-5], self.rootCert ):
            self.certData = data[:-5]
            print(self.certData)
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
    
    def codeValid(self, data):
        return data.decode('utf-8').startswith('200 ')

    def getEncryptedSymetricKey(self):
        toEncrypt = b"200 " + self.key + b'\r\n' + self.vector

        try:
            encryptedData = RsaEncryption.encrypt(
                self.getPublicKey(),
                toEncrypt
            )
            return encryptedData
        except ValueError:
            return False 

    def sslCommunication(self):
        if( not self.verifyCert() ): #receive and verify certificate
            return False

        self.genSymetricKey() #gen symetric key and vector
        key = self.getEncryptedSymetricKey() #encrypt keys with server public key

        if( key != False ): #if encryption successfull
            self.sock.sendall( key+b'\r\n\r\n' ) #send encrypted keys to server
            data = self.waitForData() #wait for server response

            return self.codeValid(data)
        else:
            return False


        

        


        
            
        