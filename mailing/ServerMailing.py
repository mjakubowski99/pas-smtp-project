import re
from database.DB import DB
import os
import datetime


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

    def getMessageResponse(self):
        response = b""
        while not b".\r\n\r\n" in response:
            response += self.client.recv(1)
        return self.decryptData(response[:-5])

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
        self.client.sendall(self.encryptData("121 Send sender adress"))
        sender = self.getResponse()
        self.client.sendall(self.encryptData("200 OK"))
        return sender[11:]

    def getRecipient(self):
        self.client.sendall(self.encryptData("122 Send recipient adress"))
        recipient = ""
        while True:
            recipient = self.getResponse()
            recipient = recipient[9:]
            if not self.checkEmail(recipient):
                self.client.sendall(self.encryptData("301 Wrong e-mail syntax"))
                
            elif not self.mailInDatabase(recipient):
                self.client.sendall(self.encryptData("402 Recipient not found"))
            else:
                self.client.sendall(self.encryptData("200 OK"))
                break
        return recipient
    
    def getSubject(self):
        self.client.sendall(self.encryptData("123 Send subject "))
        subject = self.getResponse()
        self.client.sendall(self.encryptData("200 OK"))
        return subject[9:]

    def getData(self):
        self.client.sendall(self.encryptData("124 Send data, ending with one blank line and END"))
        data = self.getMessageResponse()
        self.client.sendall(self.encryptData("200 OK"))
        return data[6:]

    def getNumberOfAttachments(self):
        self.client.sendall(self.encryptData("125 Send number of attachments"))
        data = self.getResponse()
        try:
            data = int(data)
            if data < 0:
                raise ValueError
            self.client.sendall(self.encryptData("200 OK"))
            return data
        except ValueError as err:
            self.client.sendall( self.encryptData("521 bad attachment number") )
            return -1

    def getAttachmentSize(self, response):
        data = response.split('\r\n')
        size = data[0]
        size = int(size[16:])
        return size

    def getAttachmentName(self, response):
        data = response.split('\r\n')
        filename = data[1]
        filename = filename[10:]
        return filename

    def decryptFile(self, message):
        decryptedData = self.cipher.decryptFile(message)
        return decryptedData

    def getFile(self, size):
        file = b""
        while len(file) < size:
            file += self.client.recv(1)

        return self.decryptFile(file[:-4])

    def getAttachments(self, number, recipient):
        attachments = []
        for i in range(0, number):
            self.client.sendall(self.encryptData("126 Send attachment number {}".format(i)))
            response = self.getResponse()
            size = self.getAttachmentSize(response)
            filename = self.getAttachmentName(response)
            self.client.sendall(self.encryptData("200 OK"))
            response = self.getFile(size)
            path = "attachments/" + recipient
            if not os.path.exists("attachments"):
                os.mkdir("attachments")

            if not os.path.exists(path):
                os.mkdir(path)
            
            #TODO Rozróżnić pliki o takiej samej nazwie
            #date = datetime.datetime.now().strftime("D=%Y-%m-%dT=%H:%M:%S")
            path += '/' + filename #+ date

            f = open(path, "wb")
            f.write(response)
            attachments.append(path)

        return attachments

    def getUserId(self, user):
        self.db.exec("SELECT id FROM users WHERE email=%s", (user,) )
        for x in self.db.result:
            return x 

    def sendMail(self, sender, recipient, subject, data, attachments):
        senderID = self.getUserId(sender)
        senderID = int(senderID[0])
        recipientID = self.getUserId(recipient)
        recipientID = int(recipientID[0])
        
        now = datetime.datetime.now()
        messageID = self.db.insert(
            """INSERT INTO messages (id, sender_id, receiver_id, subject, message, created_at, updated_at) 
             VALUES (0, %s, %s, %s, %s, %s, %s)""", (senderID, recipientID, subject, data, now, now) 
        )
        
        for i in attachments:
            self.db.insert(
                """INSERT INTO message_attachments (id, message_id, attachment_path, created_at, updated_at) 
                 VALUES (0, %s, %s, %s, %s)""", (messageID, i, now, now) 
            )

    def saveLogs(self, message):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        logs = open("ServerLogs.txt", "a+")
        message += '\n'
        logs.write(now+message)
        logs.close()

    def communication(self):
        sender = self.getSender()
        print("Sender = " + sender)
        
        recipient = self.getRecipient()
        print ("Recipient = " + recipient)

        subject = self.getSubject()
        print ("Subject = " + subject)

        data = self.getData()
        print ("Data = " + data)

        numberOfAttachments = self.getNumberOfAttachments()
        if( numberOfAttachments == -1 ):
            return

        print ("Number of attachments: " + str(numberOfAttachments) )

        attachments = self.getAttachments(numberOfAttachments, recipient)
        print("Attachments:")
        for i in attachments:
            print(i)

        self.sendMail(sender, recipient, subject, data, attachments)

        self.client.sendall(self.encryptData("220 Email was sent"))
        self.saveLogs(" Email from "+ sender + " to " + recipient + " was sent " + self.client.getpeername()[0])