from cryptography.hazmat.primitives.ciphers.algorithms import AES256
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives import padding
import os

class AES:
    def __init__(self, key = os.urandom(32), iv = os.urandom(16)):
        self.key = key
        self.iv = iv
        self.cipher = Cipher(AES256(self.key), CBC(self.iv))

    def encrypt(self, plaintext: str) -> bytes:
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        encryptor = self.cipher.encryptor()
        return encryptor.update(padded_data) + encryptor.finalize()
    
    def decrypt(self, ciphertext: bytes) -> str:
        decryptor = self.cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted_data.decode()
    
    @property
    def get_key(self) -> bytes:
        return self.key

    @property
    def get_iv(self) -> bytes:
        return self.iv
        