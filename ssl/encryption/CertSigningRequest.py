import ssl.encryption.RsaPrivateKeyGen as RsaPrivateKeyGen
import datetime 

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def main():
    commonName = input("Please provide your common name: ")

    RsaPrivateKeyGen.createRsaKeyFile()

    key = RsaPrivateKeyGen.rsaObject

    req = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([ 
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"PL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Lubelskie"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Lublin"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Student"),
        x509.NameAttribute(NameOID.COMMON_NAME, commonName )
    ])).sign(key, hashes.SHA256() )

    certName = input("Please provide request filename: ")
    certFile = open("ssl/reqs/"+certName, "xb")

    certFile.write(req.public_bytes(serialization.Encoding.PEM))

