import socket
import threading
import ssl.ServerSsl as ServerSsl
import ssl.encryption.SymetricEncryption as Encryption
import re
from database.DB import DB
import authentication.ServerAuthentication as ServerAuthentication
import mailing.ServerMailing as ServerMailing
import datetime

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
logs = open("ServerLogs.txt", "a+")
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
    clientIP = client.getpeername()[0]
    try:
        server = ServerSsl.ServerSsl()
        if server.sslCommunication(client): #key and vector to decryption and encryption
            saveLogs(" ssl communication done with success")
            message = server.clientKey

            cipher = Encryption.SymetricEncrypt(message)

            client.sendall(encryptData(cipher, "100 Hello supported_protocols usmtp supported_versions 1.0"))

            response = getResponse(client)
            response = decryptData(cipher, response)

            if not "1.0" in response:
                client.sendall(encryptData(cipher, "501 Unsupported version of protocol"))
                saveLogs(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Unsupported version of protocol. Connection closed. " + clientIP)
                client.close()

            authentication = ""
            while True:
                option = getResponse(client)
                option = decryptData(cipher, option)  
                print(option)  
                
                if option == "LOGIN":
                    #Authentication system
                    if authentication:
                        client.sendall(encryptData(cipher, "130 You are currently logged in"))
                        saveLogs(" Login attempt with active session " + clientIP)
                        continue
                    authenticationServer = ServerAuthentication.ServerAuthentication(client, cipher)
                    authentication = authenticationServer.communication()
                    if not authentication:
                        print("Connection close")
                        saveLogs(" Authentication failed " + clientIP)
                        saveLogs(" Connection close: " + clientIP)
                        client.close()
                elif option == "SEND MAIL":
                    #Mailing system
                    if not authentication:
                        client.sendall(encryptData(cipher, "520 Unauthorized attempt"))
                        saveLogs(" Unauthorized attempt to send mail " + clientIP)
                        saveLogs(" Connection close: " + clientIP)
                        client.close()
                    mailingServer = ServerMailing.ServerMailing(client, cipher)
                    mailingServer = mailingServer.communication()
                elif option == "BYE":
                    saveLogs(" Connection close: " + clientIP)
                    client.close()
                else:
                    client.sendall(encryptData(cipher, "300 Not recognized command"))
            
        else:
            print("Bad ssl") # Wpis do logów
            saveLogs("Bad SSLCommunication - Connection close: " + clientIP)
            client.close()
    except socket.error:
        saveLogs(" Connection close") #+ client.getpeername()[0])
        client.close()
    

def saveLogs(message):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs = open("ServerLogs.txt", "a+")
    message = time + message + '\n'
    logs.write(message)
    logs.close()
    
def listen(s):
    
    while True:
        client, addr = s.accept()
        saveLogs(" Connected client: " + addr[0])
        task = threading.Thread(target=server, kwargs={'client': client} )
        task.start()
    


s6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s6.bind(('::1', 1337))
s6.listen(5)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 1338))
s.listen(5)

task = threading.Thread(target=listen, kwargs={'s': s6} ) #ipv6 thread
task.start()

task = threading.Thread(target=listen, kwargs={'s': s} ) #ipv4 thread
task.start()


