import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class BlackBox:
	def __init__(self):
		self.backend = default_backend()
		self.rsaPrivateKey = ""
		self.rsaTheirPublicKey = ""

	def generateRandomKey(self):
		key = os.urandom(32)
		return key

	def encrypt_plaintext(self, plaintext, key):
		iv = os.urandom(16)
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
		encrypt_box = cipher.encryptor()
		ciphertext = encrypt_box.update(plaintext) + encrypt_box.finalize()
		return ciphertext, iv

	def decrypt_ciphertext(self, ciphertext, key, iv):
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
		decrypt_box = cipher.decryptor()
		plaintext = decrypt_box.update(ciphertext) + decrypt_box.finalize()
		return plaintext

	def getHMAC(self, message, key):
		tag = hmac.HMAC(key_i, hashes.SHA512(), backend=default_backend())
		tag.update(message)
		return tag.finalize(), key_i

	def rsa_encrypt(self, keys_cat):
		rsaPrivateKey = rsa.generate_private_key(public_exponent=65537,
			key_size = 2048,
			backend = default_backend())
		rsaPublicKey = rsaPrivateKey.public_key()
		cipher_keys = public_key.encrypt(
			keys_cat,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA3()),
				algorithm=hashes.SHA3(),
				label = None)
			)
		return cipher_keys

	def rsa_decrypt(self, cipher_keys):
		keys_cat = rsaPrivateKey.decrypt(
			cipher_keys,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA3()),
				algorithm=hashes.SHA3(),
				label = None)
			)
		return keys_cat

	def pgp_encap(self, message, public_key):
		key_e  = generateRandomKey()
		ciphertext, iv = encrypt_plaintext(message, key_e)
		key_i = generateRandomKey()
		tag = getHMAC(ciphertext, key_i)
		keys_cat = str(key_e) + str(key_i)
		cipher_keys = rsa_encrypt(keys_cat)
		full_ciphertext = keys_cat + ciphertext + str(tag)
		return full_ciphertext

	def pgp_decap(self, ciphertext, cipher_keys, iv, tag):
		keys_cat = rsa_decrypt(cipher_keys)
		key_e = keys_cat[:32]
		message = decrypt_ciphertext(ciphertext, key_e, iv)
		tag_t = getHMAC(ciphertext, key_cat[32:])
		if(tag_t != tag):
			print("Authentification failed")
			return
		return message
