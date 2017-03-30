from cryptography.fernet import Fernet

class BlackBox:
	def generateKey(self):
		key = Fernet.generate_key()
		f = Fernet(key)
		return f

	def encrypt_plaintext(self, plaintext, fernObj):
		ciphertext = fernObj.encrypt(plaintext)
		return ciphertext

	def decrypt_ciphertext(self, ciphertext, fernObj):  
		plaintext = fernObj.decrypt(ciphertext)
		return plaintext

	def __init__(self):
		return
