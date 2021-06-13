from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.x509.base import Certificate
from cryptography.exceptions import InvalidSignature

def getPublicKey(file):
    return serialization.load_pem_public_key(
        file
    )

def verifyCertificate(certificate, caPublicKeyFile):
    caPublicKey = getPublicKey(caPublicKeyFile)
    try:
        pass
    except Exception:
        print("RootCert Exception")
        return False 

    try:
        cert = x509.load_pem_x509_certificate(certificate)
    except Exception:
        print("Cert Exception")
        return False

    try:
        caPublicKey.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm
        )
        return True 
    except InvalidSignature:
        return False 
    


