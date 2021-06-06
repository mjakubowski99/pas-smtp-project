import socket
import ssl.ClientSsl as ClientSsl 
import ssl.encryption.SymetricEncryption as Encryption
import sys


def encryptData(encryptor, message):
    encryptedData = encryptor.encrypt(message)
    encryptedData += b"\r\n\r\n"
    return encryptedData

def decryptData(decryptor, message):
    decryptedData = decryptor.decrypt(message)
    #decryptedData = decryptedData.decode()
    decryptedData = decryptedData.replace('\r\n\r\n', '')
    #decryptedData = decryptedData[1:]
    return decryptedData

def getResponse(s):
    response = b""
    while not b"\r\n\r\n" in response:
        response += s.recv(1024)

    return response[:-4]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect( ('127.0.0.1', 1338) )

    client = ClientSsl.ClientSsl(s, open("ssl/certs/cert.pem", "rb") )
    if not client.sslCommunication():
        print("Ssl communication failed")
        s.close()
    else:
        cipher = Encryption.SymetricEncrypt(client.key, "")

        response = b""
        while not b"\r\n\r\n" in response:
            response += s.recv(1024)
        
        print(decryptData(cipher, response))

        s.sendall(encryptData(cipher, "1.0 Hello"))

        #Authentication

        authentication = False
        while not authentication:
            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response)
            if "501" in response:
                s.close()
                sys.exit(0)

            email = input("Wprowadź swój adres e-mail:\n")

            s.sendall(encryptData(cipher, email))

            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response)

            while "301" in response:
                email = input("Wprowadź swój adres e-mail:\n")
                s.sendall(encryptData(cipher, email))
                response = getResponse(s)
                response = decryptData(cipher, response)
                print(response)

            password = input("Wprowadź swoje hasło\n")

            s.sendall(encryptData(cipher, password))
            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response)
            if "200" in response:
                authentication = True
            elif "501" in response:
                sys.exit(0)

        print("OK")
        s.close()
except socket.error:
    print("500 Cannot connect to server")