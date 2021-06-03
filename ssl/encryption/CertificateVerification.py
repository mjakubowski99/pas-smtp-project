from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.x509.base import Certificate
from cryptography.exceptions import InvalidSignature

def verifyCertificate(certificate, rootCertData):
    #try:
    cert = x509.load_pem_x509_certificate(certificate)
    rootCert = x509.load_pem_x509_certificate(rootCertData)
    #except Exception:
    #    return False 
        
    key = rootCert.public_key()

    try:
        key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm
        )
        return True 
    except InvalidSignature:
        return False 
    


