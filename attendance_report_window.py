from email.mime import text
import tkinter as tk
from tkinter import*
from tkinter import ttk
import os
from datetime import datetime
from tkinter import messagebox
import mysql.connector as mysql
from tkcalendar import Calendar

#connecting to database
db = mysql.connect(host='localhost',user='root',password='', database='face_recog_attendance_db')
dbcursor = db.cursor()

class Report_Win:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.config(bg='#808080')
        self.window.state('zoomed')
        #Creating widgets
        #Frame,buttons and entrybox
        self.left_frame = tk.Frame(self.window, bg='#808080')
        self.left_frame.pack(side=LEFT, padx=(80,0), pady=(50, 50), anchor=NW)
        # Add Calendar
        self.calend = Calendar(self.left_frame, selectmode = 'day',year = 2022, month = 5,day = 1)
        self.calend.grid(row=0, column=1, pady=(12,2))
        self.subj_name_label = tk.Label(self.left_frame, text='Select Subject', font=('Helvitica', 12, 'bold'), bg='#808080')
        self.subj_name_label.grid(row=2, column=0,pady=(20,0),sticky=NW)
        self.date_label = tk.Label(self.left_frame, text='Select Date', font=('Helvitica', 12, 'bold'), bg='#808080')
        self.date_label.grid(row=0, column=0, pady=(12,0), sticky=NW)
        self.ok_button = tk.Button(self.left_frame, text='OK',command=self.enter_date)
        self.ok_button.grid(row=1, column=1, padx=5,sticky=E)
        self.view_button = tk.Button(self.left_frame, text='VIEW', command=self.view, width=15)
        self.view_button.grid(row=4, column=1, padx=5, pady=(40,10),sticky=W)
        self.exit_button = tk.Button(self.left_frame, text='EXIT', width=15,command=self.exit_window)
        self.exit_button.grid(row=5, column=1, padx=5,sticky=W)

        # query from database
        dbcursor.execute("SELECT subject_code FROM class")
        listbox_value = dbcursor.fetchall()
        #Creating Listbbox
        listbox_subjects = tk.Listbox(self.left_frame, height=len(listbox_value), selectmode=SINGLE)
        listbox_subjects.bind('<<ListboxSelect>>', self.select_subject)
        listbox_subjects.grid(row=2, column=1,padx=5,pady=(20,40),sticky=W)
        #insert values to listbox
        for val in listbox_value:
            listbox_subjects.insert(END, val[0])
        #Creating attendance table
        self.table_frame = tk.Frame(self.window)
        self.table_frame.pack(side=RIGHT, padx=(20,80), pady=(75,50), anchor=NE)
        #scrollbar
        self.table_scrollbar = tk.Scrollbar(self.table_frame)
        self.table_scrollbar.pack(side=RIGHT, fill=Y)
        #Table
        self.attendance_table = ttk.Treeview(self.table_frame,yscrollcommand=self.table_scrollbar.set)
        self.attendance_table.pack(side=TOP, anchor=N)
        self.table_scrollbar.config(command=self.attendance_table.yview)
        #define table columns
        self.attendance_table['columns'] = ('student_lastname', 'student_firstname','student_middlename', 'subject_code', 'attend_date_time')
        #format columns
        self.attendance_table.column('#0', width=0, stretch=0)
        self.attendance_table.column('student_lastname', anchor=CENTER, width=180)
        self.attendance_table.column('student_firstname',anchor=CENTER, width=180)
        self.attendance_table.column('student_middlename',anchor=CENTER,width=180)
        self.attendance_table.column('subject_code',anchor=CENTER,width=100)
        self.attendance_table.column('attend_date_time',anchor=CENTER,width=180)
        #Creating Headings
        self.attendance_table.heading("#0", text="",anchor=CENTER)
        self.attendance_table.heading("student_lastname", text="Student Lastname", anchor=CENTER)
        self.attendance_table.heading("student_firstname", text="Student Firstname", anchor=CENTER)
        self.attendance_table.heading("student_middlename", text="Student Middlename", anchor=CENTER)
        self.attendance_table.heading("subject_code", text="Subject Code", anchor=CENTER)
        self.attendance_table.heading("attend_date_time", text="Date Time", anchor=CENTER)   
        #Bottom Frame,buttons and entrybox
        self.right_frame = tk.Frame(self.window, bg='#808080')
        self.right_frame.pack(side=RIGHT, padx=(5,80), pady=(75,50), anchor=NE)
        self.left_frame.pack_propagate(False)
        
        self.window.mainloop()

    def enter_date(self):
        self.date_val = self.calend.selection_get()
        
    def select_subject(self,event,):
        selection = event.widget.curselection()
        index = selection[0]
        self.slectedValue = event.widget.get(index)
    def view(self):
        self.attendance_table.delete(*self.attendance_table.get_children())
        try:
            table_data = f"SELECT student.last_name, student.first_name, student.middle_name, class.subject_code,attendance.date_time_in \
                        FROM student JOIN attendance ON student.id = attendance.student_id JOIN class ON class.id = attendance.class_id \
                        WHERE subject_code = '{self.slectedValue}' AND date(date_time_in) = '{self.date_val}' ORDER BY student.last_name ASC"
            dbcursor.execute(table_data)
            tDatas = dbcursor.fetchall()
            #loop tru tuple of data
            for data in tDatas:
                self.attendance_table.insert("", 'end',iid=data[0], text=data[0],values=(data[0], data[1], data[2], data[3], data[4]))
        except AttributeError:
            messagebox.showerror("ERROR","Choose date and press 'OK'.")
        except Exception as e:
            messagebox.showerror("ERROR","error"+ e)    
    def exit_window(self):
        self.window.destroy()
        os.system('py main_window.py')
if __name__ == "__main__":
    Report_Win(tk.Tk(), "ATTENDANCE REPORT")
