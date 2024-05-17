from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__(self, key):
        self.AES = AES.new(key, AES.MODE_CBC)
    
    def encrypt(self, data):
        return self.AES.encrypt(pad(data, AES.block_size))

    def decrypt(self, enc_data):
        return unpad(self.AES.decrypt(enc_data), AES.block_size)
    
