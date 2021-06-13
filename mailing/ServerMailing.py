import re
from database.DB import DB


class ServerMailing:
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

    def getSender(self):
        self.client.sendall(self.encryptData("xxx Send sender adress"))
        sender = self.getResponse()
        self.client.sendall(self.encryptData("200 OK"))
        return sender[11:]

    def getRecipient(self):
        self.client.sendall(self.encryptData("xxx Send recipient adress"))
        recipient = ""
        while True:
            recipient = self.getResponse()
            recipient = recipient[9:]
            if not self.checkEmail(recipient):
                self.client.sendall(self.encryptData("301 Wrong e-mail syntax"))
                break
            elif not self.mailInDatabase(recipient):
                self.client.sendall(self.encryptData("xxx Recipient not found"))
                break
            else:
                self.client.sendall(self.encryptData("200 OK"))
                break
        return recipient
    
    def getSubject(self):
        self.client.sendall(self.encryptData("xxx Send subject "))
        subject = self.getResponse()
        self.client.sendall(self.encryptData("200 OK"))
        return subject[9:]

    def getData(self):
        self.client.sendall(self.encryptData("xxx Send data, ending with one blank line and END"))
        data = self.getResponse()
        self.client.sendall(self.encryptData("200 OK"))
        return data[6:]

    #def getNumberOfAttachments(self):
    #    self.client.sendall(self.encryptData("xxx Send number of attachments"))
    #    data = self.getResponse()
    #    self.client.sendall(self.encryptData("200 OK"))
    #   return data

    #def getAttachments(self, number):
        
    #    print("ok")

    def getUserId(self, user):
        self.db.exec("SELECT id FROM users WHERE email=%s", (user,) )
        for x in self.db.result:
            return x 


    def sendMail(self, sender, recipient, subject, data):
        senderID = self.getUserId(sender)
        senderID = int(senderID[0])
        recipientID = self.getUserId(recipient)
        recipientID = int(recipientID[0])

        self.db.insert("INSERT INTO messages (id, sender_id, receiver_id, subject, message, created_at, updated_at) VALUES (0, %s, %s, %s, %s, null, null)", (senderID, recipientID, subject, data,) ) 

    def communication(self):
        sender = self.getSender()
        print("Sender = " + sender)
        
        recipient = self.getRecipient()
        print ("Recipient = " + recipient)

        subject = self.getSubject()
        print ("Subject = " + subject)

        data = self.getData()
        print ("Data = " + data)

        self.sendMail(sender, recipient, subject, data)

    #    numberOfAttachments = self.getNumberOfAttachments()
    #    print (int(numberOfAttachments))





        