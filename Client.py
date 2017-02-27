import time

class Client:

	def start_up(self):
		start_up_input = raw_input("Select Option:\n1. Create New Account\n2. Log In\n")
		if start_up_input == "1":
			username = raw_input("Create Username: ")
			password = raw_input("Create Password: ")
			check = self.create_new_user(username, password)
			if check == False:
				print("Could not create user...terminating")
				time.sleep(5)
				return
			print("User account created\n")
		elif start_up_input == "2":
			username = raw_input("Username: ")
			password = raw_input("Password: ")
			check = self.log_in(username, password)
			if check == False:
				print("Could not log in...terminating")
				time.sleep(5)
				return
			print("Log in Successful\n")
		else:
			print("Error: Invalid Input...terminating")
			time.sleep(5)
		while True:
			if self.check_for_message():
				print("Message: \n")
			msg = raw_input("Send Message? (Y/N): ")
			if msg.upper() == "Y":
				recipient = raw_input("Send to: ")
				msg = raw_input("> ")
				self.sendMessage(recipient, msg)
			else:
				print("Checking for message...\n")

	def check_for_message(self):
		return True

	def create_new_user(self, username, password):
		#store to database
		return True

	def log_in(self, username, password):
		#check w/ database
		return True

	def sendMessage(self, recipient, message):

		return True

	def __init__(self):
		self.start_up()
		return
def main():
    client = Client()

if __name__ == "__main__":
    main()
