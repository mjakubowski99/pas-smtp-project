from os import system
import socket
import ssl.ServerSsl as ServerSsl
import ssl.encryption.SymetricEncryption as Encryption
import re
from database.DB import DB

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

db = DB()

def mailInDatabase(mail):
    db.exec("SELECT email FROM users WHERE email=%s", (mail,) )
    for x in db.result:
        return True
    return False 

def getResponse(client):
    response = b""
    while not b"\r\n\r\n" in response:
        response += client.recv(1)
    return response[:-4]

def encryptData(encryptor, message):
    encryptedData = encryptor.encrypt(message)
    encryptedData += b"\r\n\r\n"
    return encryptedData

def decryptData(decryptor, message):
    decryptedData = decryptor.decrypt(message)
    return decryptedData

def checkEmail(email):
    if(re.search(regex, email)):
        return True
    else:
        return False

def authClient(email, password):
    if email == "jan.kowalski@wp.pl" and password == "supersilnehaslo":
        return True
    return False

def validHeader(response, header):
    return response.startswith(header)

def receiveMail(client, cipher):
    response = decryptData(cipher, getResponse(client) )

    if( not validHeader(response, "mail from: ") ):
        client.sendall( encryptData(cipher, "400 bad sender header") )
        client.close()
        return False 

    sender = response[11:]
    print(sender)
    if not checkEmail(sender):
        client.sendall( encryptData(cipher, "400 bad mail pattern") )
        client.close()
        return False 

    if not mailInDatabase(sender):
        client.sendall( encryptData(cipher, "400 bad mail") )
        client.close()
        return False 

    client.sendall( encryptData(cipher, "200 ok go recipients") )
    return True

    
    
    




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1338))
s.listen(5)

while True:
    client, addr = s.accept()
    print("Connected: ", addr[0])

    try:
        server = ServerSsl.ServerSsl()
        if server.sslCommunication(client): #key and vector to decryption and encryption
            message = (server.clientKey, server.clientVector)

            cipher = Encryption.SymetricEncrypt(message[0], "")

            client.sendall(encryptData(cipher, "100 Hello supported_protocols usmtp supported_versions 1.0"))

            response = getResponse(client)
            response = decryptData(cipher, response)

            if not "1.0" in response:
                client.sendall(encryptData(cipher, "503 Unsupported version of protocol"))
                client.close()

            #Authentication system
            authentication = False
            counter = 0
            while not authentication:
                counter += 1
                if(counter == 5):
                    client.sendall(encryptData(cipher, "501 Multiple wrong login or password. Try again later."))
                    client.close()
                    break
                client.sendall(encryptData(cipher, "111 Send your e-mail adress"))

                response = getResponse(client)
                response = decryptData(cipher, response)
                email = response
                print(checkEmail(email))
                while not checkEmail(email):
                    print("petla")
                    client.sendall(encryptData(cipher, "301 Wrong e-mail syntax"))
                    response = getResponse(client)
                    response = decryptData(cipher, response)
                    email = response

                client.sendall(encryptData(cipher, "112 Send your password"))

                response = getResponse(client)
                response = decryptData(cipher, response)
                password = response

                authentication = authClient(email, password)
                if not authentication:
                    client.sendall(encryptData(cipher, "401 Wrong password"))
                else:
                    break

            if authentication:
                client.sendall(encryptData(cipher, "200 Authentication successful"))
                print("Authentication successful")

                receiveMail(client, cipher)
        else:
            print("Bad ssl")
            client.close()
    except socket.error:
        client.close()

    client.close()


