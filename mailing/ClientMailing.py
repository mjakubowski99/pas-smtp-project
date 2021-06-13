
class ClientMailing:
    def __init__(self, s, cipher, sender):
        self.s = s
        self.cipher = cipher
        self.sender = sender

    def getResponse(self):
        response = b""
        while not b"\r\n\r\n" in response:
            response += self.s.recv(1)
        return self.decryptData(response[:-4])

    def encryptData(self, message):
        encryptedData = self.cipher.encrypt(message)
        encryptedData += b"\r\n\r\n"
        return encryptedData

    def decryptData(self, message):
        decryptedData = self.cipher.decrypt(message)
        return decryptedData

    def prepareMessage(self, data, header):
        header += data
        return header

    def sendSender(self, email):
        response = self.getResponse()
        print(response[4:])
        self.s.sendall( self.encryptData(self.prepareMessage(email, "mail from: ") ) )
        response = self.getResponse()
        print(response[4:])

    def sendRecipient(self):
        response = self.getResponse()
        print(response[4:])
        #TODO dodatkowa walidacja
        email = input()
        self.s.sendall( self.encryptData(self.prepareMessage(email, "mail to: ") ) )
        response = self.getResponse()
        print(response[4:])       

    def sendSubject(self):
        response = self.getResponse()
        print(response[4:])
        subject = input()
        self.s.sendall( self.encryptData(self.prepareMessage(subject, "subject: ") ) )
        response = self.getResponse()
        print(response[4:])  

    def sendData(self):
        response = self.getResponse()
        print(response[4:])
        data = self.inputData()
        self.s.sendall( self.encryptData(self.prepareMessage(data, "data: ") ) )
        response = self.getResponse()
        print(response[4:])

    def inputData(self):
        data = ""
        while True:
            data += input() + '\n'
            if '\n\nEND' in data:
                break
        return data[:-6]

    def sendAttachments(self):
        response = self.getResponse()
        print(response[4:])
        number = input()
        self.s.sendall( self.encryptData(number) )
        response = self.getResponse()
        print(response[4:])


    def communication(self):
        self.sendSender(self.sender)
        self.sendRecipient()
        self.sendSubject()
        self.sendData()
        
        #self.sendAttachments()




        

        