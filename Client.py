import time
import sys
import requests
import threading
import Queue
from Tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, END, DISABLED, NORMAL, VERTICAL, Scrollbar
from ttk import Frame, Label, Entry, Button

def check_for_message(queue, username, password):
	user = username
	psw = password
	time.sleep(5)
	while True:
 		#req = requests.get("https://seenada.thereyougo.co/get_message", 
 		#	auth={'username': user, 'password': psw})
 		#if req.status_code != 200:
 		#	print("Error when checking for message\n")
		#for item in req.text:
		#	message = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp'])) + "-" + item['from_user'] + ": " + item['content'] + "\n"
		#	if message != None: 
		#		queue.put(message)
		queue.put("test")
		time.sleep(.5)
 	return

class Client:
 
 	def __init__(self, parent, queue):
 		self.start_up()
 		self.parent = parent
 		self.parent.protocol('WM_DELETE_WINDOW', self.exitApp)
 		self.queue = queue
		self.msgEntry = Text(self.parent, borderwidth=2,height=10,width=50)
		self.msgTxt = Text(self.parent, height=10, width=50)
		self.msgTxt.config(state=DISABLED)
		self.parent.title("Seenada")
		self.setUpGUI()
		self.username = ""
		self.password = ""
 		return

 	def exitApp(self):
 		print("\nTerminating Background Thread....")
 		self.msg_thread.join()
 		self.parent.destroy()
 		return

 	def start_up(self):
 		#req = requests.get("https://seenada.thereyougo.co/")
 		#if req != 200:
 	#		print("Could Not Connect To Server....terminating\n")
 		#	time.sleep(3)
 		#	return
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
		self.msg_thread = threading.Thread(target=check_for_message, args=(self.queue, self.username, self.password))
		self.msg_thread.start()

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
 		recipient = recEntry.get()
 		message = msgEntry.get()
 		timestamp = int(time.time())
  		req = requests.post("https://seenada.thereyougo.co/send_message",
 			data={'from': self.username, 'to': recipient, 'content': message, 'timestamp': timestamp})
 		if req.status_code != 200:
 			print("Error when trying to send message")
 			return False
 		self.recEntry.delete(0, END)
 		self.msgEntry.delete(0, END)
 		print("Message Sent")
 		return True

  	def create_new_user(self, username, password):
 		#req = requests.post("https://seenada.thereyougo.co/signup", 
 		#	data={'username':username, 'password':password})
 		#if req.status_code != 200:
 		#	print("Error when creating user account\n")
 		#	return False
 		self.username = username
 		self.password = password
 		return True
 
 	def log_in(self, username, password):
 		#req = requests.post("https://seenada.thereyougo.co/signin",
 		#	data={'username': username, 'password':password})
 		#if req.status_code != 200:
 		#	print("Error when trying to log in")
 		#	return False
 		self.username = username
 		self.password = password
 		return True


def main():
	queue = Queue.Queue()
	root = Tk()
	root.withdraw()
	root.geometry("500x475")
	app = Client(root, queue)
	root.mainloop()

 
if __name__ == "__main__":
     main()
