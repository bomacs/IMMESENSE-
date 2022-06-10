import tkinter as tk
from tkinter import *
from tkinter import ttk
import mysql.connector as mysql

# connect to database
db = mysql.connect(host='localhost',user='root',password='', database='face_recog_attendance_db')  
dbcursor = db.cursor()

class Users:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.config(bg='#808080')
        #self.window.state('zoomed')

        #Creating widgets
        #Frame
        self.frame = tk.Frame(self.window, bg='#808080')
        self.frame.pack(side=TOP, anchor=CENTER, pady=150)
        #Labels
        self.user_type_label = tk.Label(self.frame, text="User Role", font=('Helvitica', 12, 'bold'), bg="#808080")
        self.user_type_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.last_name_label = tk.Label(self.frame, text="Last Name", font=('Helvitica', 12, 'bold'), bg="#808080")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.first_name_label = tk.Label(self.frame, text="First Name", font=('Helvitica', 12, 'bold'), bg="#808080")
        self.first_name_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.middle_name_label = tk.Label(self.frame, text="Middle Name", font=('Helvitica', 12, 'bold'), bg="#808080")
        self.middle_name_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.username_label = tk.Label(self.frame, text="Username", font=('Helvitica', 12, 'bold'), bg="#808080")
        self.username_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.password_label = tk.Label(self.frame, text="Password", font=('Helvitica', 12, 'bold'), bg="#808080")
        self.password_label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
        #Entryboxes
        self.user_type_entry = tk.Entry(self.frame, width=30)
        self.user_type_entry.grid(row=0, column=1, columnspan=2, ipady=2, padx=10)
        self.last_name_entry = tk.Entry(self.frame, width=30)
        self.last_name_entry.grid(row=1, column=1, columnspan=2, ipady=2, padx=10)
        self.first_name_entry = tk.Entry(self.frame, width=30)
        self.first_name_entry.grid(row=2, column=1, columnspan=2, ipady=2, padx=10)
        self.middle_name_entry = tk.Entry(self.frame, width=30)
        self.middle_name_entry.grid(row=3, column=1, columnspan=2, ipady=2, padx=10)
        self.username_entry = tk.Entry(self.frame, width=30)
        self.username_entry.grid(row=4, column=1, columnspan=2, ipady=2, padx=10)
        self.password_entry = tk.Entry(self.frame, width=30)
        self.password_entry.grid(row=5, column=1, columnspan=2, ipady=2, padx=10)

        #Buttons
        self.save_button = tk.Button(self.frame, text='Save',command=self.add_user, width=10)
        self.save_button.grid(row=6, column=1, padx=6, pady=30)
        self.save_button = tk.Button(self.frame, text='Exit',command=self.window.destroy, width=10)
        self.save_button.grid(row=6, column=2, padx=6, pady=30)

        #Create window
        self.window.mainloop()
        #Methods
        # method to save entries
    def add_user(self):
        role_id = self.user_type_entry.get()
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        #Connect to database
        user_info = "INSERT INTO user(username, user_lastname, user_firstname, user_middlename, user_role, password) VALUES (%s, %s, %s, %s, %s, %s)"
        dbcursor.execute(user_info,(username, last_name, first_name, middle_name, role_id, password))
        db.commit()
        db.close()
        #Clear entry fields after entries are saved
        self.user_type_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.first_name_entry.delete(0,END)
        self.middle_name_entry.delete(0,END)
        self.username_entry.delete(0,END)
        self.password_entry.delete(0,END)
       
Users(tk.Tk(), "User Sign Up")
