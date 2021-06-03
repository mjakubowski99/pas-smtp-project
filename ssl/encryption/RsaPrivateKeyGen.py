from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

filename = '' 
rsaObject = None 

def genPrivateRsaKey():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

def createRsaKeyFile():
    rsaKey = genPrivateRsaKey()

    global rsaObject
    rsaObject = rsaKey

    keyFilename = input("Let's provide filename which will be rsa key filename: ")
    passphrase = input("Please provide passphrase used to encryption: ")

    keyFile = open("certs/"+keyFilename, "wb")

    filename = keyFilename

    keyFile.write(
        rsaKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption( passphrase.encode('utf-8') )
        )
    )
    print("Rsa private key generated")

