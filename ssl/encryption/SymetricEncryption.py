from os import system
from ssl.encryption.RsaEncryption import encrypt
from typing import Counter
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class SymetricEncrypt:
    def __init__(self, key, vector):
        self.howManyAdd = 0 
        self.key = key
        self.cipher = Cipher( algorithms.AES(key), modes.ECB() )

    def addSpacesToMessage(self, message, howManyAdd):
        for x in range(0, howManyAdd):
            message += " "
        return message

    def formatMessage(self, message):
        length = len(message)
        if( length < 16):
            self.howManyAdd = 16 - length
        elif( length % 16 != 0 ):
            self.howManyAdd = 16 - (length%16)

        #print("Dodalem " + str(self.howManyAdd) + " bialych znakow do napisu: " + message)

        #if self.howManyAdd < 11:
        #    self.howManyAdd -= 1
        #else:
        #    self.howManyAdd -= 2
        #message = str(self.howManyAdd) + message
        #print(message)
        #print(len(message))

        return self.addSpacesToMessage(message, self.howManyAdd)
    
    def encrypt(self, message):
        encryptor = self.cipher.encryptor()
        return encryptor.update( self.formatMessage(message).encode('utf-8') ) + encryptor.finalize()

    def formatFile(self, message):
        length = len(message)
        if( length < 16):
            self.howManyAdd = 16 - length
        elif( length % 16 != 0 ):
            self.howManyAdd = 16 - (length%16)

        for x in range(0, self.howManyAdd):
            message += b" "
        return message

    def encryptFile(self, message):
        encryptor = self.cipher.encryptor()
        return encryptor.update( self.formatFile(message)) + encryptor.finalize()

    def decryptFile(self, message):
        decryptor = self.cipher.decryptor()
        message = decryptor.update(message)
        message = message.decode()
        counter = self.calc(message)
        #print("Znalzlem " + str(counter) + " bialych znakow w napisie: " + message)
        return message[:-counter].encode()

    def calc(self, message):
        counter = len(message) - 1
        whitechars = 0
        while counter >= 0:
            if message[counter] == " ":
                counter -= 1
                whitechars += 1
            else:
                break
        return whitechars

    def calcBinary(self, message):
        counter = len(message) - 1
        whitechars = 0
        while counter >= 0:
            if message[counter] == b" ":
                counter -= 1
                whitechars += 1
            else:
                break
        return whitechars

    def decrypt(self, message):
        decryptor = self.cipher.decryptor()
        message = decryptor.update(message)
        message = message.decode()
        counter = self.calc(message)
        #print("Znalzlem " + str(counter) + " bialych znakow w napisie: " + message)
        return message[:-counter]

    
