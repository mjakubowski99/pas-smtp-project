import socket
import threading
import ssl.ServerSsl as ServerSsl
import ssl.encryption.SymetricEncryption as Encryption
import re
from database.DB import DB
import authentication.ServerAuthentication as ServerAuthentication
import mailing.ServerMailing as ServerMailing

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

def server(client):
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
            authenticationServer = ServerAuthentication.ServerAuthentication(client, cipher)
            authentication = authenticationServer.communication()
            if not authentication:
                print("Connection close: ", addr[0]) # Wpis do logów
                client.close()

            #Mailing system
            mailingServer = ServerMailing.ServerMailing(client, cipher)
            mailingServer = mailingServer.communication()
            
        else:
            print("Bad ssl") # Wpis do logów
            print("Connection close: ", addr[0]) # Wpis do logów
            client.close()
    except socket.error:
        client.close()
    
    
    
def listen(s):
    while True:
        client, addr = s.accept()
        print("Connected: ", addr[0]) # Wpis do logów

        task = threading.Thread(target=server, kwargs={'client': client} )
        task.start()
    


s6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s6.bind(('::1', 1337))
s6.listen(5)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1338))
s.listen(5)

task = threading.Thread(target=listen, kwargs={'s': s6} )
task.start()

task = threading.Thread(target=listen, kwargs={'s': s} )
task.start()


