import os.path
import sys

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
    
    def test(self, message):
        encryptedData = self.cipher.encrypt(message)
        #encryptedData += b"\r\n\r\n"
        return encryptedData       

    def encryptData(self, message):
        #message += "\r\n\r\n"
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
        if response.startswith("520"):
            sys.exit(0)
        self.s.sendall( self.encryptData(self.prepareMessage(email, "mail from: ") ) )
        response = self.getResponse()
        print(response[4:])

    def sendRecipient(self):
        response = self.getResponse()
        print(response[4:])
        while not response.startswith("200"):
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

    def encryptFile(self, data):
        encryptedData = self.cipher.encryptFile(data)
        encryptedData += b"\r\n\r\n"
        return encryptedData

    def sendAttachments(self):
        response = self.getResponse()
        print(response[4:])
        number = input()
        self.s.sendall( self.encryptData(number) )
        response = self.getResponse()
        if( not response.startswith("200 ") ):
            print(response)
            self.s.close()
            sys.exit(0)

        print(response[4:])

        try:
            number = int(number)
            for i in range(0, number):
                response = self.getResponse()
                print(response[4:])
                while True:
                    filename = input("Input filename:\n")
                    if os.path.isfile(filename):
                        break
                    else:
                        print("File " + filename + " not found.\n")

                file = open(filename, "rb")
                data = file.read()
                data = self.encryptFile(data)
                message = "Content-Length: "+ str(len(data)) + "\r\n" + "Filename: " + filename
                self.s.sendall( self.encryptData(message) )
                response = self.getResponse()
                print(response[4:])
                self.s.sendall( data )
        except ValueError:
            self.s.close()
            sys.exit(0)



    def communication(self):
        self.sendSender(self.sender)
        self.sendRecipient()
        self.sendSubject()
        self.sendData()
        self.sendAttachments()
        
        response = self.getResponse()
        print(response[4:])




        

        