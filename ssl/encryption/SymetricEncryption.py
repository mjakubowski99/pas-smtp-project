from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class SymetricEncrypt:
    def __init__(self, key, vector):
        self.howManyAdd = 0 
        self.cipher = Cipher( algorithms.AES(key), modes.ECB() )

    def addSpacesToMessage(self, message, howManyAdd):
        for x in range(0, howManyAdd):
            message += " "
        return message

    def formatMessage(self, message):
        length = len(message)
        if( length < 16):
            self.howManyAdd = 16 - length
        elif( length%16 != 0 ):
            self.howManyAdd = 16 - (length%16)
        
        return self.addSpacesToMessage(message, self.howManyAdd)
    
    def encrypt(self, message):
        encryptor = self.cipher.encryptor()
        return encryptor.update( 
            self.formatMessage(message).encode('utf-8') 
        ) + encryptor.finalize()

    def decrypt(self, message):
        decryptor = self.cipher.decryptor()
        message = decryptor.update(message)
        return message[:-self.howManyAdd]
