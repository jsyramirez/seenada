import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class BlackBox:
	def __init__(self):
		self.backend = default_backend()

	def generateRandomKey(self):
		key = os.urandom(256)
		return key

	def encrypt_plaintext(self, plaintext, key):
		iv = os.urandom(128)
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
		encrypt_box = cipher.encryptor()
		ciphertext = encrypt_box.update(plaintext) + encrypt_box.finalize()
		return ciphertext, iv

	def decrypt_ciphertext(self, ciphertext, key, iv):
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
		decrypt_box = cipher.decryptor()
		plaintext = decrypt_box.update(ciphertext) + decrypt_box.finalize()
		return plaintext
