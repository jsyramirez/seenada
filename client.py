import time
import sys
import base64
import requests
import threading
import Queue
import json
import hmac
import binascii
import scrypt
import hashlib
import binascii
from Tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, END, DISABLED, NORMAL, VERTICAL, Scrollbar
from ttk import Frame, Label, Entry, Button
from tkFileDialog import askopenfilename
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac as chmac
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat

class BlackBox:
	def __init__(self):
		self.backend = default_backend()
		self.rsaMyPublicKey = ""
		self.rsaTheirPublicKey = ""
		self.rsaPrivateKey = rsa.generate_private_key(public_exponent=65537,
			key_size = 2048,
			backend = default_backend())
		self.rsaMyPublicKey = self.rsaPrivateKey.public_key()
		self.printPublicKey()
		#print(self.rsaMyPublicKey.public_bytes(Encoding('PEM'), PublicFormat('X.509 subjectPublicKeyInfo with PKCS#1')))
		file = open("public_key.pem", "w")
		file_write = (self.rsaMyPublicKey.public_bytes(Encoding('PEM'), PublicFormat('X.509 subjectPublicKeyInfo with PKCS#1')))
		file.write(file_write)
		file.close()


	def printPublicKey(self):
		pem = self.rsaMyPublicKey.public_bytes(encoding=Encoding.PEM,format=PublicFormat.SubjectPublicKeyInfo)
		#print(pem.splitlines())
		return pem
		#return self.rsaMyPublicKey.public_bytes(Encoding('PEM'), PublicFormat('X.509 subjectPublicKeyInfo with PKCS#1'))

	def generateRandomKey(self):
		key = os.urandom(32)
		return key

	def encrypt_plaintext(self, plaintext, key):
		iv = os.urandom(16)
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
		encrypt_box = cipher.encryptor()
		#b_plaintext = ''.join(format(ord(y), 'b') for y in plaintext)
		#b_plaintext = bytes(plaintext)
		#print(b_plaintext)
		#b_plaintext = binascii.a2b_base64(plaintext)
		#>>> y = binascii.b2a_base64(r)
		ciphertext = encrypt_box.update(bytes(plaintext)) + encrypt_box.finalize()
		#print("OG Ciphertext: " + ciphertext)
		#print("OG IV: " + iv)
		print "length of ciphertext"
		print len(ciphertext)
		return ciphertext, iv

	def decrypt_ciphertext(self, ciphertext, key, iv):
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
		decrypt_box = cipher.decryptor()
		plaintext = decrypt_box.update(ciphertext) + decrypt_box.finalize()
		#plaintext = binascii.b2a_base64(b_plaintext)
		return plaintext

	def getHMAC(self, message, key):
		tag = chmac.HMAC(key, hashes.SHA512(), backend=self.backend)
		tag.update(message)
		return tag.finalize()

	def rsa_encrypt(self, keys_cat):
		#b_keys_cat = ''.join(format(ord(y), 'b') for y in keys_cat)
		#print "plaintext"
		#print keys_cat
		cipher_keys = self.rsaTheirPublicKey.encrypt(
			keys_cat,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA512()),
				algorithm=hashes.SHA512(),
				label = None)
			)
		#print("OG Cipher Keys: " + cipher_keys + " len of cipher key: " + str(len(cipher_keys)))
		return cipher_keys

	def rsa_decrypt(self, cipher_keys):
		keys_cat = self.rsaPrivateKey.decrypt(
			cipher_keys,
			padding.OAEP(
				mgf=padding.MGF1(algorithm=hashes.SHA512()),
				algorithm=hashes.SHA512(),
				label = None)
			)
		print("Cipher Keys? " + keys_cat)
		return keys_cat

	def pgp_encap(self, message):
		key_e  = self.generateRandomKey()
		print "length of padded message"
		print len(self.padMessage(message))
		ciphertext, iv = self.encrypt_plaintext(self.padMessage(message), key_e)
		key_i = self.generateRandomKey()
		tag = self.getHMAC(ciphertext, key_i)
		keys_cat = str(key_e) + str(key_i)
		cipher_keys = self.rsa_encrypt(keys_cat)
		full_ciphertext = cipher_keys + iv + tag + ciphertext
		print "clent information"
		print("key_e" + key_e)
		print("key_i" + key_i)
		print("Tag: " + tag)
		print("Full CipherText: " + full_ciphertext)
		return full_ciphertext

	def pgp_decap(self, ciphertext, cipher_keys, iv, tag):
		keys_cat = self.rsa_decrypt(cipher_keys)
		key_e = keys_cat[:32]
		message = self.decrypt_ciphertext(ciphertext, key_e, iv)
		tag_t = self.getHMAC(ciphertext, keys_cat[32:])
		if(tag_t != tag):
			print "------list of tag--------"
			print tag_t
			print tag
			print("Authentification failed")
			return
		return message

	def loadTheirPublicKey(self, public_key_filename):
		file = open(public_key_filename, "r")
		key_str = file.read()
		file.close()
		self.rsaTheirPublicKey = load_pem_public_key(key_str, default_backend())

	def padMessage(self, message):
		num_pad = len(message) % 16
		if num_pad == 0:
			return message
		for i in range(0, 15):
			message = message + " "
			if len(message) % 16 == 0:
				break
		return message

def check_for_message(queue, username, tok, blackBox):
	user = username
	token = tok
	print token
	time.sleep(5)
	while True:
		headers = {'Auth': token}
		resp = requests.get('https://seenada.thereyougo.co/get_message', headers=headers)
		if resp.status_code != 200:
			print("Error when checking for message\n")
		for item in json.loads(resp.text):
			#ciphertext = item['message']
			#print item['message'].encode('ascii','ignore')
			#ciphertext = base64.b64decode(item['message'])
			#print ciphertext #binascii.unhexlify(item['message'])
			ciphertext = binascii.unhexlify(item['message'])
			#full_ciphertext = keys_cat + ciphertext + str(tag) + iv
			#print(ciphertext)
			#print(len(ciphertext))
			#ciphertext = client1.pgp_encap(message)
			#print len(ciphertext)
			keys = ciphertext[:256]
			#print len(keys)
			iv  = ciphertext[256:272]
			#print len(iv)
			tag = ciphertext[272:336]
			#print ciphertext
			ctext = ciphertext[336:]
			message = blackBox.pgp_decap(ctext, keys, iv, tag)
			message = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp'])) + "-" + item['from'] + ": " + message + "\n"
			if message != None: 
				queue.put(message)
		#queue.put(resp.text)
		time.sleep(.5)
 	return

class Client:
	def __init__(self, parent, queue):
		self.blackBox = BlackBox()
		self.start_up()
		self.parent = parent
		self.parent.protocol('WM_DELETE_WINDOW', self.exitApp)
		self.queue = queue
		self.msgEntry = Text(self.parent, borderwidth=2,height=10,width=50)
		self.msgTxt = Text(self.parent, height=10, width=50)
		self.msgTxt.config(state=DISABLED)
		self.parent.title("Seenada")
		self.setUpGUI()
		return

	def exitApp(self):
		print("\nTerminating Background Thread....")
		#self.msg_thread.join()
		#self.parent.destroy()
		sys.exit()
		return

	def start_up(self):
		req = requests.get("https://seenada.thereyougo.co/")
		if req.status_code != 200:
			print(req.status_code)
 			print("Could Not Connect To Server....terminating\n")
 			time.sleep(3)
 			return
 		start_up_input = raw_input("Select Option:\n1. Create New Account\n2. Log In\n")
 		if start_up_input == "1":
 			username = raw_input("Create Username: ")
 			password = raw_input("Create Password: ")
 			check = self.create_new_user(username, password)
 			check = self.log_in(username, password)
 			if check == False:
 				print("Could not create user...terminating")
 				time.sleep(3)
 				sys.exit()
 			print("User account created\n")
 			start_up_input = ""
 			return
 		elif start_up_input == "2":
 			username = raw_input("Username: ")
 			password = raw_input("Password: ")
 			check = self.log_in(username, password)
 			if check == False:
 				print("Could not log in...terminating")
 				time.sleep(3)
 				return
 			print("Log in Successful\n")
 			start_up_input = ""
 			return
 		else:
 			print("Error: Invalid Input...terminating")
 			time.sleep(3)
 			sys.exit()

	def setUpGUI(self):
		self.parent.deiconify()
		msgLbl1 = Label(self.parent, text="Messages:", width=6)
		msgLbl1.grid(row=0, column=0)
		self.msgTxt.grid(row=0, column=1, padx=10)
 		scroll_bar = Scrollbar(self.msgTxt, orient=VERTICAL, command=self.msgTxt.yview)
 		scroll_bar.config(command=self.msgTxt.yview)
 		self.msgTxt.config(yscrollcommand=scroll_bar.set)
		self.msgTxt['yscroll'] = scroll_bar.set
		recLbl = Label(self.parent, text="Send To", width=6)
		recLbl.grid(row=1, column=0)
		self.__recEntry = Entry(self.parent, width=50)
		self.__recEntry.grid(row=1, column=1, padx=10)
		msgLbl2 = Label(self.parent, text="Message", width=6)
		msgLbl2.grid(row=2, column=0)
		self.msgEntry.grid(row=2, column=1,padx=10)
		sendButton = Button(self.parent, text="Send", command=self.sendMessage)
		sendButton.grid(row=3,column=1)
		loadButton = Button(self.parent, text="Load Key", command=self.openFile)
		loadButton.grid(row=4, column=1)
		self.parent.after(1000, self.read_queue)
		self.msg_thread = threading.Thread(target=check_for_message, args=(self.queue, self.username, self.token, self.blackBox))
		self.msg_thread.start()

	def openFile(self):
		self.public_key_filename = askopenfilename()
		#file = open(self.public_key_filename, "r")
		#key_str = file.read()
		#file.close()
		self.blackBox.loadTheirPublicKey(self.public_key_filename)
		return

	def read_queue(self):
		try:
			new_msg = "\n" + self.queue.get_nowait()
			self.msgTxt.config(state=NORMAL)
			self.msgTxt.insert(END, new_msg)
			self.msgTxt.see(END)
		except Queue.Empty:
			pass
		self.parent.after(1000, self.read_queue)
 
	def sendMessage(self):
		print self.username
		headers = {"Auth": self.token}
 		recipient = self.__recEntry.get()
 		message = self.msgEntry.get("1.0",END)
 		timestamp = int(time.time())
 		ciphertext = self.blackBox.pgp_encap(message)
		msg_obj = {'from': self.username, 'to': recipient, 'msg': binascii.hexlify(ciphertext), 'time': timestamp}
		#print ciphertext
		#print binascii.hexlify(ciphertext)
  		req = requests.post("https://seenada.thereyougo.co/send_message",
 			headers=headers, data=json.dumps(msg_obj))
 		if req.status_code != 200:
 			print("Error when trying to send message")
 			return False
 		#self.__recEntry.delete(0, END)
 		self.msgEntry.delete("1.0", END)
 		print("Message Sent")
 		return True

	def create_new_user(self, username, password):
 		req = requests.post("https://seenada.thereyougo.co/register", 
 			data=json.dumps({'username':username, 'password':password}))
 		if req.status_code != 200:
 			print("Error when creating user account\n")
 			return False
 		self.username = username
 		self.password = password
 		return True
	
	def log_in(self, username, password):
		obj = {"username": username}
		step1 = requests.post('https://seenada.thereyougo.co/signin1', data=json.dumps(obj))
		if step1.status_code == 200 and 'found' not in step1.text:
			salt = (step1.json()['salt']).encode('ascii', 'ignore')
			challenge = (step1.json()['challenge']).encode('ascii', 'ignore')
			hashed_password = binascii.hexlify(scrypt.hash(password, salt))
			tag = hmac.new(hashed_password, challenge, hashlib.sha512).hexdigest()
			obj2 = {"username": username, "tag": tag, "challenge": challenge}
			step2 = requests.post('https://seenada.thereyougo.co/signin2', data=json.dumps(obj2))
			if step2.status_code == 200:
				self.username = username
				self.password = password
				self.token = step2.text
				print self.username
				return True
		else:
			print "check your credential"
			return False

def main():
	queue = Queue.Queue()
	root = Tk()
	root.withdraw()
	root.geometry("500x475")
	app = Client(root, queue)
	root.mainloop()

if __name__ == "__main__":
     main()