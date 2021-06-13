import datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import cryptography.hazmat.primitives.serialization as serialization


def main():
    rootCertData = open("ssl/rootCert/cert.pem", "rb")
    try:
        issuer = x509.load_pem_x509_certificate(rootCertData.read())
    except Exception:
        print("RootCert Exception")
        return False 

    keyData = open("ssl/keys/root.pem", "rb")
    rootKey = load_pem_private_key(keyData.read(), password=b"pass123")
    
    req = input("Please provide cert signing request filename: ")
    reqFile = open("ssl/reqs/"+req, "rb")
    try:
        subject = x509.load_pem_x509_csr(reqFile.read())
    except Exception:
        print("Cert Exception")
        return False

    
    cert = x509.CertificateBuilder().subject_name(
        subject.subject
    ).issuer_name(
        issuer.subject
    ).public_key(
        subject.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after( 
        datetime.datetime.utcnow() + datetime.timedelta(days=300)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(rootKey, hashes.SHA256())

    certName = input("Please provide filename for new stored certificate: ")

    try:
        certFile = open("ssl/certs/"+certName, "xb")
        certFile.write(cert.public_bytes(serialization.Encoding.PEM))
    except FileExistsError as ex:
        print("This filename already exists! Failed to sign cert")
        return False

    print("Certificate successfully signed")
    return True
