import tkinter as tk
from tkinter import messagebox, filedialog
from emailv import check_mail
from keygen import generate_keys
from googleAuth import Authenticate
from imagemanipulation import Image_Encryption, Image_Decryption
from server_side_methods.db.Cassandra import Cassandra_db
import uuid
from uuid import UUID
import json
from send_email import create_message, sendEmail

LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 8)


class GUI(tk.Tk):

    def __init__(self):
        super().__init__()
        container = tk.Frame(self)

        container.pack()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(3, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, SendingPageService, D3Page, DNAPage, RecievingPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def popup(msg1, msg2):
    messagebox.showinfo(msg1, msg2)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Google Login", font=LARGE_FONT)
        label.grid(pady=10, padx=10)
        button1 = tk.Button(self, text="Login Via Google",
                            command=lambda: [Authenticate(), popup("Information", "Login Successful"),
                                             controller.show_frame(PageOne)])
        button1.grid()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Choose Service", font=LARGE_FONT)
        label.grid(pady=10, padx=10)
        button1 = tk.Button(self, text="Send Image to a recipient",
                            command=lambda: controller.show_frame(SendingPageService))
        button2 = tk.Button(self, text="Receive an Image", command=lambda: controller.show_frame(RecievingPage))
        button1.grid()
        button2.grid()


class SendingPageService(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select the Type of Encryption", font=LARGE_FONT)
        label.grid(pady=10, padx=10)
        button1 = tk.Button(self, text="Tripe DES Encryption", command=lambda: controller.show_frame(D3Page))
        button2 = tk.Button(self, text="DNA Encryption", command=lambda: controller.show_frame(DNAPage))
        button3 = tk.Button(self, text="Go back to choosing services", command=lambda: controller.show_frame(PageOne))
        button1.grid()
        button2.grid()
        button3.grid()


class RecievingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Enter the shared UUID and Key", font=LARGE_FONT)
        label.grid(pady=10, padx=10)

        label2 = tk.Label(self, text="Enter the shared UUID ", font=MEDIUM_FONT)
        label2.grid(row=2, column=0)
        self.uuid = tk.Entry(self)
        self.uuid.grid(row=2, column=1)

        label3 = tk.Label(self, text="Enter the shared key ", font=MEDIUM_FONT)
        label3.grid(row=3, column=0)
        self.key = tk.Entry(self)
        self.key.grid(row=3, column=1)

        label4 = tk.Label(self, text="Enter the path to save the image ", font=MEDIUM_FONT)
        label4.grid(row=4, column=0)
        self.path = tk.Entry(self)
        self.path.grid(row=4, column=1, padx=2)

        label5 = tk.Label(self, text="Enter the name of the image ", font=MEDIUM_FONT)
        label5.grid(row=5, column=0)
        self.name = tk.Entry(self)
        self.name.grid(row=5, column=1)

        button1 = tk.Button(self, text="Get Image", command=lambda: self.check_details(controller))
        button3 = tk.Button(self, text="Go back to choosing services", command=lambda: controller.show_frame(PageOne))
        button1.grid()
        button3.grid()

    def check_details(self, controller):
        jsonData = {'uuid': self.uuid.get(), 'key': self.key.get()}
        jsonData2 = json.dumps(jsonData)

        db = Cassandra_db('d3', 'ikd')
        r = db.get(jsonData2)
        if not r:
            messagebox.showerror("Checking Details", "The keys and uuid doesnt match or doesnt exist in the DB, they get deleted after an hour of submission!")
        enc = bytes.fromhex(r[0]['data'])
        Image_Decryption(enc,self.key.get(), self.path.get(), self.name.get())





class D3Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        heading = tk.Label(self, text="Verify Recipient's Email id", font=MEDIUM_FONT)
        heading.grid(row=0, columnspan=4)

        label2 = tk.Label(self, text="Enter Recipient's Email id", font=MEDIUM_FONT)
        label2.grid(row=1)
        self.input = tk.Entry(self)
        self.input.grid(row=2)
        button1 = tk.Button(self, text="Check", command=lambda: self.mail_check(controller))
        button1.grid(row=2, column=1)

        label = tk.Label(self, text="Select Image to Encrypt", font=MEDIUM_FONT)
        label.grid(row=3, column=0, columnspan=3, pady=10, padx=10)
        button2 = tk.Button(self, text="Select Image", command=lambda: self.take_image(controller))
        button2.grid(row=5, column=0)
        label2 = tk.Label(self, text="Enter 24-bit Encryption Key", font=MEDIUM_FONT)
        label2.grid(row=6, column=0)

        self.e = tk.Entry(self)
        self.e.grid(row=7)
        button4 = tk.Button(self, text="Check Key", command=lambda: self.check_key(controller))
        button4.grid(row=7, column=1)
        button4 = tk.Button(self, text="Generate Key", command=lambda: self.gen_key())
        button4.grid(row=7, column=2)
        button3 = tk.Button(self, text="Go back to choosing services", command=lambda: controller.show_frame(PageOne))
        button3.grid(row=9, column=0)

    def mail_check(self, controller):
        self.recipient = self.input.get()
        self.valid_mail = check_mail(self.recipient)
        if self.valid_mail:
            popup("Email Id check", "Valid Email ID")
        else:
            popup("Email Id check", "Invalid Email ID")

    def take_image(self, controller):
        self.filename = filedialog.askopenfile(title="Select Image")
        label1 = tk.Label(self, text=self.filename.name, font=MEDIUM_FONT)
        label1.grid(row=4)

    def check_key(self, controller):
        if len(self.e.get()) == 24:
            popup("Encryption Key Check", "Key is valid")
            button2 = tk.Button(self, text="Encrypt", command=lambda: [self.encrypt(), controller.show_frame(PageOne)])
            button2.grid(row=8, column=0)
        else:
            messagebox.showerror("Encryption Key Check", "Key is invalid")

    def gen_key(self):
        self.e.delete(0, tk.END)
        self.key = generate_keys(24)
        self.e.insert(0, self.key)

    def encrypt(self):
        if len(self.e.get()) != 24:
            messagebox.showerror("Encryption Key Check", "Key is invalid, Retry Again!")
        else:
            self.enc = Image_Encryption(self.filename.name, self.key)
            jsonData = {'uuid': uuid.uuid4().hex, 'key': self.key, 'data': self.enc.hex()}
            jsonData2 = json.dumps(jsonData)
            db = Cassandra_db('d3', 'ikd')
            db.add(jsonData2)
            result = db.get(jsonData2)
            if result:
                messagebox.showinfo("Server Status", "Data Stored in Server Successfully")
            else:
                messagebox.showerror("Server Status", "Data Stored in Server Unsuccessfully")

            message = create_message(self.recipient, jsonData)
            m = sendEmail(message)
            if result:
                messagebox.showinfo("Email Status", "Email sent to Recipient")
            else:
                messagebox.showerror("Email Status", f"Unable to send email to Recipient:\n {m}")


class DNAPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Under Construction", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button3 = tk.Button(self, text="Go back to choosing services", command=lambda: controller.show_frame(PageOne))
        button3.pack()


app = GUI()
app.mainloop()
# def send_or_recieve():
#     choice = Toplevel(login)
#
#
#
# global login
#
# login = Tk()
# login.geometry("500x500")
# login.title("Login")
#
# my_label = Label(login, text="Authenticate Via Gmail Login", bg="gray", width="500", height="2")
# my_label.grid()
# Label(text="").grid()
# Button(login, text="Google Login", width="30", height="2", command=Authenticate).grid()
# send_or_recieve(login)
# login.mainloop()
# print(service)
