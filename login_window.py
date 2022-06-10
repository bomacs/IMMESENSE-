import tkinter
from tkinter import *
from tkinter import messagebox
import mysql.connector as mysql
import os

try:
    db1 = mysql.connect(host='localhost',user='root',password='', database='face_recog_attendance_db')  
except Exception:
    messagebox.showerror("Connection Failed", "Database server is closed.")

class Login_window():   
    def __init__(self,window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.config(bg='#808080')
        self.window.state("zoomed")

    
        # Heading "Admin Login" container
        self.heading_frame = Frame(self.window, bg='#808080')
        self.heading_frame.pack(pady=(150,0))

        option = {'padx':5,'pady':5}
       
        self.label_heading = Label(self.heading_frame,
            text="ADMIN LOGIN",
            font=('Helvitica',40,'bold'),
            bg='#a6a6a6')
        self.label_heading.pack()

        # username and password container
        self.username_password_frame = Frame(self.window, bg='#808080')
        self.username_password_frame.pack(pady=20)
        
        self.label_username = Label(self.username_password_frame,
            text='User Name:',
            font=('Helvitica',15,'bold'),
            bg='#808080')
        self.label_username.grid(row=0, column=0, **option)
        self.label_password = Label(self.username_password_frame,
            text='Password:',
            font=('Helvitica',15,'bold'),
            bg='#808080')
        self.label_password.grid(row=1, column=0, **option)
     
        self.entrybox_username = Entry(self.username_password_frame)
        self.entrybox_username.grid(row=0, column=1, ipadx=20, ipady=5, **option)
        self.entrybox_password = Entry(self.username_password_frame, show="*")
        self.entrybox_password.grid(row=1, column=1, ipadx=20, ipady=5, **option)

        #Buttons login and signup container
        self.buttons_frame1 = Frame(self.window, bg='#808080')
        self.buttons_frame1.pack(pady=15, padx=(20,0))
        
        self.login_button = Button(self.buttons_frame1,text="Login",command=self.verify_login, width=10)
        self.login_button.pack(side=LEFT, padx=(100,0))
        self.signup_button = Button(self.buttons_frame1, text="Signup", command=self.signup, width=10)
        self.signup_button.pack(side=RIGHT, padx=(12,0)) 

        #Forgot Password button container
        self.fgotpassword_frame = Frame(self.window)
        self.fgotpassword_frame.pack(side=RIGHT, padx=(0,20), pady=(200,0))
        
        self.fgotpassword_button = Button(self.fgotpassword_frame, text="Forgot Password", command=self.forgot_password)
        self.fgotpassword_button.pack()

        self.window.mainloop()
     
    # function to verify login
    def verify_login(self):
        user_name = self.entrybox_username.get()
        pssword = self.entrybox_password.get()
        dbcursor = db1.cursor()
        login_data = "SELECT * FROM user WHERE BINARY username = %s AND BINARY password = %s"
        dbcursor.execute(login_data,(user_name,pssword))
        result = dbcursor.fetchmany()

        if result:
            #clear entry box
            self.entrybox_username.delete(0, END)
            self.entrybox_password.delete(0,END)

            messagebox.showinfo("Welcome "+ user_name , "Login Success!!")
            self.window.destroy()
            os.system('py main_window.py')
        # elif len(result) == 0:
        #     messagebox.showerror("LOGIN FAILED ", "Incorrect username or password!")
        else:
            messagebox.showerror("LOGIN FAILED ", "Incorrect username or password!")
            #return 0

    def signup(self):
        os.system('py signup_window.py')

    def forgot_password(self):
        pass     
       
if __name__ == '__main__':
    app = Login_window(tkinter.Tk(),"IMMESENSE Face Resognition Attendance System")
