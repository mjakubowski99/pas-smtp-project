#from server import receiveMail
import socket
import ssl.ClientSsl as ClientSsl 
import ssl.encryption.SymetricEncryption as Encryption
import sys
import mailing.ClientMailing as ClientMailing


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

def prepareMessage(data, header):
    header += data
    return header 

#def sendMail(s, cipher, data, header):
#    s.sendall( encryptData(cipher, prepareMessage(data, header) ) )
#    response = decryptData( cipher, getResponse(s) )
#    print(response)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect( ('127.0.0.1', 1338) )
    client = ClientSsl.ClientSsl(s, open("ssl/clientKeys/rootPublicKey.pem", "rb") )
    if not client.sslCommunication():
        print("Ssl communication failed")
        s.close()
    else:
        print("Ssl communication ended with success")
        cipher = Encryption.SymetricEncrypt(client.key)

        response = b""
        while not b"\r\n\r\n" in response:
            response += s.recv(1024)
        
        print(decryptData(cipher, response))

        s.sendall(encryptData(cipher, "1.0 Hello"))

        authentication = False
        email = ""
        while True:
            message = input("Choose operations:\n")
            s.sendall(encryptData(cipher, message))

            if message == "LOGIN":
                #Authentication
                if authentication:
                    response = getResponse(s)
                    response = decryptData(cipher, response)
                    print(response[4:])
                while not authentication:
                    response = getResponse(s)
                    response = decryptData(cipher, response)
                    print(response[4:])
                    if response.startswith("510"):
                        s.close()
                        sys.exit(0)

                    email = input()

                    s.sendall(encryptData(cipher, email))

                    response = getResponse(s)
                    response = decryptData(cipher, response)
                    print(response[4:])
                    if "510" in response:
                        s.close()
                        sys.exit(0)
                    

                    while "301" in response:
                        email = input()
                        s.sendall(encryptData(cipher, email))
                        response = getResponse(s)
                        response = decryptData(cipher, response)
                        print(response[4:])
                        if "510" in response:
                            s.close()
                            sys.exit(0)

                    password = input()

                    s.sendall(encryptData(cipher, password))
                    response = getResponse(s)
                    response = decryptData(cipher, response)
                    print(response[4:])
                    if "210" in response:
                        authentication = True
                    elif "510" in response:
                        sys.exit(0)
            elif message == "SEND MAIL":
                clientMailing = ClientMailing.ClientMailing(s, cipher, email)
                clientMailing = clientMailing.communication()
            elif message == "BYE":
                s.close()
                sys.exit(0)
            else:
                response = getResponse(s)
                response = decryptData(cipher, response)
                print(response[4:])

        #Authentication
        authentication = False
        while not authentication:
            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response[4:])
            if "510" in response:
                s.close()
                sys.exit(0)

            email = input()

            s.sendall(encryptData(cipher, email))

            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response[4:])
            if "510" in response:
                s.close()
                sys.exit(0)
            

            while "301" in response:
                email = input()
                s.sendall(encryptData(cipher, email))
                response = getResponse(s)
                response = decryptData(cipher, response)
                print(response[4:])
                if "510" in response:
                    s.close()
                    sys.exit(0)

            password = input()

            s.sendall(encryptData(cipher, password))
            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response[4:])
            if "210" in response:
                authentication = True
                #sendMail(s, cipher, email, "mail from: ")
                #sendMessage(email, "mail from: ")
            elif "510" in response:
                sys.exit(0)
        clientMailing = ClientMailing.ClientMailing(s, cipher, email)
        clientMailing = clientMailing.communication()
        s.close()
except socket.error:
    print("500 Cannot connect to server")