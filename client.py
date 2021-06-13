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
            print(response[4:])
            if "501" in response:
                s.close()
                sys.exit(0)

            email = input()

            s.sendall(encryptData(cipher, email))

            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response[4:])
            if "501" in response:
                s.close()
                sys.exit(0)
            

            while "301" in response:
                email = input()
                s.sendall(encryptData(cipher, email))
                response = getResponse(s)
                response = decryptData(cipher, response)
                print(response[4:])
                if "501" in response:
                    s.close()
                    sys.exit(0)

            password = input()

            s.sendall(encryptData(cipher, password))
            response = getResponse(s)
            response = decryptData(cipher, response)
            print(response[4:])
            if "200" in response:
                authentication = True
                #sendMail(s, cipher, email, "mail from: ")
                #sendMessage(email, "mail from: ")
            elif "501" in response:
                sys.exit(0)
        clientMailing = ClientMailing.ClientMailing(s, cipher, email)
        clientMailing = clientMailing.communication()
        s.close()
except socket.error:
    print("500 Cannot connect to server")
    '''
        recipient = input("Wprowadź adres e-mail odbiorcy:\n")
        sendMail(s, cipher, recipient, "mail to: ")
        #sendMessage(recipient, "mail to: ")

        subject = input("Wprowadź temat wiadomości:\n")
        sendMail(s, cipher, subject, "subject: ")
        #sendMessage(subject, "subject: ")


        print("Wprowadź dane:\nW celu zakończenia wprowadzania danych zostaw jedną linię pustą, a w kolejnej wpisz wyraz END\n")
        data = ""
        while True:#not '\rEND\n' in line:
            data += input() + '\n'
            if '\n\nEND' in data:
                break
        data = data[:-6]
        sendMail(s, cipher, data, "data: ")
        #sendMessage(recipient, "data: ")
'''