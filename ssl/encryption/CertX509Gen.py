import ssl.encryption.RsaPrivateKeyGen as RsaPrivateKeyGen
import datetime 

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

RsaPrivateKeyGen.createRsaKeyFile()

commonName = input("Please provide your common name: ")

subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"PL"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Lubelskie"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Lublin"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"UMCS"),
    x509.NameAttribute(NameOID.COMMON_NAME, commonName )
])

issuer = subject

cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    RsaPrivateKeyGen.rsaObject.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after( 
    datetime.datetime.utcnow() + datetime.timedelta(days=300)
).add_extension(
    x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
    critical=False,
).sign(RsaPrivateKeyGen.rsaObject, hashes.SHA256())

certName = input("Please provide certificate filename: ")
certFile = open("certs/"+certName, "wb")

certFile.write(cert.public_bytes(serialization.Encoding.PEM))




