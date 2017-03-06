import time
import threading
import sys
from select import select


class Client:	
	def start_up(self):
		start_up_input = raw_input("Select Option:\n1. Create New Account\n2. Log In\n")
		if start_up_input == "1":
			username = raw_input("Create Username> ")
			password = raw_input("Create Password> ")
			check = self.create_new_user(username, password)
			if check == False:
				print("Could not create user...terminating")
				time.sleep(2)
				return
			print("User account created\n")
		elif start_up_input == "2":
			username = raw_input("Username> ")
			password = raw_input("Password> ")
			check = self.log_in(username, password)
			if check == False:
				print("Could not log in...terminating")
				time.sleep(2)
				return
			print("Log in Successful\n")
		else:
			print("Error: Invalid Input...terminating")
			time.sleep(2)
			sys.exit()
		#t = threading.Thread(target=self.prompt_for_message)
		#self.threads.append(t)
		#t.start()
		self.prompt_for_message()
		self.check_for_message()
		return

	#foreground thread waiting for user to send message
	def prompt_for_message(self):
		timeout = 15
		print(self.options)
		rlist, _, _ = select([sys.stdin], [], [], timeout)
		if rlist:
			s = sys.stdin.readline()
			recipient = raw_input("Send to> ")
			msg = raw_input("Enter Message> ")
			msg_sent = self.sendMessage(recipient, msg)
			if msg_sent == False:
				print("Message Sent!\n")
			else:
				print("Could not send message, user: " + recipient + ", does not exist\n")
				time.sleep(1)
		else:
			print "No input. Moving on..."
			threading.Timer(1,self.prompt_for_message).start()
		#while(True):
		#	try:
		#		if raw_input_with_timeout(prompt, timeout=30.0) = "send":
		#			recipient = raw_input("Send to> ")
		#			msg = raw_input("Enter Message> ")
		#			msg_sent = self.sendMessage(recipient, msg)
		#			if msg_sent == False:
		#				print("Message Sent!\n")
		#			else:
		#				print("Could not send message, user: " + recipient + ", does not exist\n")
		#			time.sleep(1)
		#	except KeyboardInterrupt:
		#		print("\nKeyboardInterrupt catched.")
		#		print ("Terminate main thread.")
		return

	#background thread to check for messages
	def check_for_message(self):
		#check w/ database
		sender = 2 #TEMPORARY
		msg_recvd = 2 #TEMPORARY
		#while(True):
		try:
			time.sleep(1)
			if (msg_recvd % 2 == 0) and (sender % 2 ==  0):
				print(str(sender) + "> " + str(msg_recvd))
				msg_recvd = msg_recvd + 1
				sender = sender + 1
			threading.Timer(5,self.check_for_message).start()
		except KeyboardInterrupt:
			print("\nKeyboardInterrupt catched.")
			print ("Terminate main thread.")
		return

	def create_new_user(self, username, password):
		#store to database
		return True

	def log_in(self, username, password):
		#check w/ database
		return True

	def sendMessage(self, recipient, message):
		#store to database
		return True

	def __init__(self):
		self.options = "\nOptions:\nTo send a message, type \"send\"\nTo exit, type \"exit\"\n"
		self.threads = []
		self.start_up()    
		return

def main():
	client = Client()
	try:
		kill_threads(client.threads)
	except KeyboardInterrupt:
		print("\nKeyboardInterrupt catched.")
		print ("Terminate main thread.")

def kill_threads(threads):
	for t in threads:
			t.join()

if __name__ == "__main__":
    main()
