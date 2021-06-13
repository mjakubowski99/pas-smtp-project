import re
from database.DB import DB
import hashlib


class ServerAuthentication:
    def __init__(self, client, cipher):
        self.client = client
        self.cipher = cipher
        self.emailRegex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        self.db = DB()

    def getResponse(self):
        response = b""
        while not b"\r\n\r\n" in response:
            response += self.client.recv(1)
        return self.decryptData(response[:-4])

    def encryptData(self, message):
        encryptedData = self.cipher.encrypt(message)
        encryptedData += b"\r\n\r\n"
        return encryptedData

    def decryptData(self, message):
        decryptedData = self.cipher.decrypt(message)
        return decryptedData

    def checkEmail(self, email):
        if(re.search(self.emailRegex, email)):
            return True
        else:
            return False

    def mailInDatabase(self, mail):
        self.db.exec("SELECT email FROM users WHERE email=%s", (mail,) )
        for x in self.db.result:
            return True
        return False 

    def authentication(self, email, password):
        self.db.exec("SELECT email, password FROM users WHERE email = %s AND password = %s", (email, password,) )
        for x in self.db.result:
            return True
        return False

    def communication(self):
        authentication = False
        counter = 0
        while not authentication:
            counter += 1
            if(counter >= 6):
                self.client.sendall(self.encryptData("501 Multiple wrong login or password. Try again later.")) #Wpis do logów
                return False
            self.client.sendall(self.encryptData("111 Send your e-mail adress"))

            response = self.getResponse()
            email = response
            
            while not self.checkEmail(email):
                print("petla")
                counter += 1
                self.client.sendall(self.encryptData("301 Wrong e-mail syntax"))
                response = self.getResponse()
                email = response
                if(counter >= 6):
                    self.client.sendall(self.encryptData("501 Multiple wrong login or password. Try again later.")) #Wpis do logów
                    return False

            self.client.sendall(self.encryptData("112 Send your password"))

            response = self.getResponse()
            sha = hashlib.sha256()
            sha.update(response.encode())
            password = sha.hexdigest()

            authentication = self.authentication(email, password)

            if not authentication:
                self.client.sendall(self.encryptData("401 Wrong password")) #Wpis do logów
            else:
                break

        if authentication:
            self.client.sendall(self.encryptData("200 Authentication successful"))
            print("Authentication successful") #Wpis do logów
            return True