import time
import sys
import requests
import threading
import Queue
from Tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, END, DISABLED, NORMAL, VERTICAL, Scrollbar
from ttk import Frame, Label, Entry, Button

class Client:
 
 	def __init__(self, parent, queue):
 		self.start_up()
 		self.parent = parent
 		self.queue = queue
		self.msgEntry = Text(self.parent, borderwidth=2,height=10,width=50)
		self.msgTxt = Text(self.parent, height=10, width=50)
		self.msgTxt.config(state=DISABLED)
		self.parent.title("Seenada")
		self.setUpGUI()
 		return

 	def start_up(self):
 		req = requests.get("https://seenada.thereyougo.co/")
 		if req != 200:
 			print("Could Not Connect To Server....terminating\n")
 			time.sleep(3)
 			return
 		start_up_input = raw_input("Select Option:\n1. Create New Account\n2. Log In\n")
 		if start_up_input == "1":
 			username = raw_input("Create Username: ")
 			password = raw_input("Create Password: ")
 			check = self.create_new_user(username, password)
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
		recLbl.grid(row=1,column=0)
		recEntry = Entry(self.parent,width=50)
		recEntry.grid(row=1, column=1,padx=10)
		msgLbl2 = Label(self.parent, text="Message", width=6)
		msgLbl2.grid(row=2, column=0)
		self.msgEntry.grid(row=2, column=1,padx=10)
		sendButton = Button(self.parent, text="Send", command=self.sendMessage)
		sendButton.grid(row=3,column=1)
		self.parent.after(1000, self.read_queue)

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
 		print("Message Sent\n")
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

def check_for_message(queue):
	time.sleep(5)
	i = 0
	while True:
		new_message = "False" #replace w/ call to server
		if new_message != None: 
			print("Checking for messages...")
			queue.put(new_message + str(i))
			i = i + 1
		time.sleep(.5)
 	return


def main():
	queue = Queue.Queue()
	msg_thread = threading.Thread(target=check_for_message, args=(queue,))
	msg_thread.start()
	root = Tk()
	root.withdraw()
	root.geometry("500x500")
	app = Client(root, queue)
	root.mainloop()

 
if __name__ == "__main__":
     main()
