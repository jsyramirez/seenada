import time
import requests
from Tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT
from ttk import Frame, Label, Entry, Button
 

class ClientGUI:
  
	def __init__(self, parent):
		self.parent = parent
		parent.title("Seenada")
		self.setUpGUI()

	def setUpGUI(self):
		msgLbl1 = Label(self.parent, text="Messages:", width=6)
		msgLbl1.grid(row=0, column=0)
		msgTxt = Label(self.parent,text="message_test",borderwidth=2,width=50)
		msgTxt.grid(row=0, column=1, padx=10)
		recLbl = Label(self.parent, text="Send To", width=6)
		recLbl.grid(row=1,column=0)
		recEntry = Entry(self.parent,width=50)
		recEntry.grid(row=1, column=1,padx=10)
		msgLbl2 = Label(self.parent, text="Message", width=6)
		msgLbl2.grid(row=2, column=0)
		msgEntry = Text(self.parent, borderwidth=2,height=10,width=50)
		msgEntry.grid(row=2, column=1,padx=10)
		sendButton = Button(self.parent, text="Send", command=self.sendMessage)
		sendButton.grid(row=3,column=1)
	def sendMessage(self):
		print("Message Sent\n")
		return

class Client:
 
 	def start_up(self):
 		req = requests.get("https://seenada.thereyougo.co/")
 		if req != 200:
 			print("Could Not Connect To Server....terminating\n")
 			time.sleep(5)
 			return
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
 		req = requests.post("https://seenada.thereyougo.co/signup", 
 			data={'username':username, 'password':password})
 		if req.status_code != 200:
 			print("Error when creating user account\n")
 			return False
 		return True
 
 	def log_in(self, username, password):
 		req = requests.post("https://seenada.thereyougo.co/signin",
 			data={'username': username, 'password':password})
 		if req.status_code != 200:
 			print("Could not Log In")
 			return False
 		return True
 
 	def sendMessage(self, recipient, message):
 		return True
 
 	def __init__(self):
 		self.start_up()
 		return
def main():
	client = Client()
	root = Tk()
	root.geometry("500x250")
	app = ClientGUI(root)
	root.mainloop()  
 
if __name__ == "__main__":
     main()
