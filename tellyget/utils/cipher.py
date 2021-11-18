from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad


class Cipher:
    def __init__(self, key):
        self.cipher = DES.new(key.encode(), DES.MODE_ECB)

    def encrypt(self, plain_text):
        cipher_text = self.cipher.encrypt(pad(plain_text.encode(), DES.block_size))
        return cipher_text.hex().upper()

    def decrypt(self, cipher_text):
        plain_text = unpad(self.cipher.decrypt(bytes.fromhex(cipher_text)), DES.block_size)
        return plain_text.decode()
