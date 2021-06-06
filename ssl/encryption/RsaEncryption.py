
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
#from cryptography import x509
#from cryptography.hazmat.primitives import serialization

def encrypt(key, message):
    try: 
        encryptedData = key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encryptedData
    except ValueError:
        return False

def decrypt(key, message):
    try:
        decryptedData = key.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ),
        )
        return decryptedData
    except ValueError:
        return False 

#certificate = open("ssl/certs/cert.pem", "rb")

#cert = x509.load_pem_x509_certificate( certificate.read() )
#private_key = serialization.load_pem_private_key(
#    private.read(),
#    password=b"pass123"
#)


#key = cert.public_key()

#print( decrypt( private_key,encrypt(key, b"123") ) )

