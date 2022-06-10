import tkinter as tk
from tkinter import*
from tkinter import messagebox, ttk
import os
import mysql.connector as mysql

#connecting to database
db = mysql.connect(host='localhost',user='root',password='', database='face_recog_attendance_db')
dbcursor = db.cursor()

# Class to create window
class Class_Info:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.config(bg='#808080')
        self.window.state('zoomed')
        #Creating frames
        self.widgets_frame = tk.Frame(self.window, background='#808080')
        self.widgets_frame.pack(side=LEFT, padx=(80,0), pady=(50, 50), anchor=NW)
        self.widgets_frame.pack_propagate(False)
        self.total_subject_label = tk.Label(self.widgets_frame, text="Total Subjects:", font=('Helvitica', 12, 'bold'),background="#808080")
        self.total_subject_label.grid(row=0,column=0, sticky=W)
        self.subject_label = tk.Label(self.widgets_frame, text="Subjects", font=('Helvitica', 12, 'bold'),background="#808080")
        self.subject_label.grid(row=1, column=0, pady=10, sticky=NW)
        # query from database
        dbcursor.execute("SELECT subject_code FROM class")
        self.listbox_value = dbcursor.fetchall()
        #label
        self.no_subject_label = tk.Label(self.widgets_frame, text=len(self.listbox_value), font=('Helvitica', 12, 'bold'),background="#ffffff")
        self.no_subject_label.grid(row=0, column=1, sticky=W)
       
        #Creating Listbbox
        listbox_subjects = tk.Listbox(self.widgets_frame, height=len(self.listbox_value), selectmode=SINGLE)
        listbox_subjects.bind('<<ListboxSelect>>', self.getSelect)
        listbox_subjects.grid(row=1, column=1, pady=12)
        #insert values to listbox
        for val in self.listbox_value:
            listbox_subjects.insert(END, val[0])
    

        #Creating other widgets
        self.dash_label1 = tk.Label(self.widgets_frame,text='-----------------------------------------------------', bg='#808080')
        self.dash_label1.grid(row=2, column=0, columnspan=2)
        self.add_subj_label = tk.Label(self.widgets_frame, text='ADD SUBJECT', font=('Helvitica',16,'bold'), bg='#808080')
        self.add_subj_label.grid(row=3, column=0, columnspan=2)
        self.dash_label2 = tk.Label(self.widgets_frame,text='-----------------------------------------------------', bg='#808080')
        self.dash_label2.grid(row=4, column=0, columnspan=2)
        self.subj_code_label = tk.Label(self.widgets_frame, text='Subject Code', font=('Helvitica',12,'bold'), bg='#808080')
        self.subj_code_label.grid(row=5, column=0, sticky=W)
        self.subj_code_entrybox = tk.Entry(self.widgets_frame,)
        self.subj_code_entrybox.grid(row=5, column=1, padx=3, pady=5)
        self.subj_name_label = tk.Label(self.widgets_frame, text='Subject Name', font=('Helvitica',12,'bold'), bg='#808080')
        self.subj_name_label.grid(row=6, column=0, sticky=W)
        self.subj_name_entrybox = tk.Entry(self.widgets_frame,)
        self.subj_name_entrybox.grid(row=6, column=1, padx=3, pady=5)
        self.subj_name_label = tk.Label(self.widgets_frame, text='Crse/yr/sec', font=('Helvitica',12,'bold'), bg='#808080')
        self.subj_name_label.grid(row=7, column=0, sticky=W)
        self.crse_yr_sec_entrybox = tk.Entry(self.widgets_frame,)
        self.crse_yr_sec_entrybox.grid(row=7, column=1, padx=3, pady=5)
        self.add_button = tk.Button(self.widgets_frame, text='ADD', command=self.add, width=10)
        self.add_button.grid(row=8, column=0, ipadx=5, ipady=2, pady=5)
        self.dash_label3 = tk.Label(self.widgets_frame,text='-----------------------------------------------------', bg='#808080')
        self.dash_label3.grid(row=9, column=0, columnspan=2)
        self.remove_subj_label = tk.Label(self.widgets_frame, text='REMOVE SUBJECT', font=('Helvitica',16,'bold'), bg='#808080')
        self.remove_subj_label.grid(row=10, column=0, columnspan=2)
        self.dash_label4 = tk.Label(self.widgets_frame,text='-----------------------------------------------------', bg='#808080')
        self.dash_label4.grid(row=11, column=0, columnspan=2)
        self.subj_id_label = tk.Label(self.widgets_frame, text='Subject Code', font=('Helvitica',12,'bold'), bg='#808080')
        self.subj_id_label.grid(row=12, column=0, sticky=W)
        self.subj_id_entrybox = tk.Entry(self.widgets_frame,)
        self.subj_id_entrybox.grid(row=12, column=1, padx=3, pady=5)
        self.remove_button = tk.Button(self.widgets_frame, text='REMOVE', command=self.remove, width=10)
        self.remove_button.grid(row=13, column=0, ipadx=5, ipady=2, pady=3)
        #back  button
        self.exit_button = tk.Button(self.widgets_frame, text="BACK", command=self.back, width=10)
        self.exit_button.grid(row=14, column=1,pady=30, sticky=E)

        #------------------Creating table for enrolled students--------------------------------
        self.table_frame = tk.Frame(self.window)
        self.table_frame.pack(side=RIGHT, padx=(5,80), pady=(75,50), anchor=NE)
        #scrollbar
        self.table_scrollbar = tk.Scrollbar(self.table_frame)
        self.table_scrollbar.pack(side=RIGHT, fill=Y)
        #Table
        self.student_table = ttk.Treeview(self.table_frame,yscrollcommand=self.table_scrollbar.set, height=500)
        self.student_table.pack(side=TOP, anchor=N)
        self.table_scrollbar.config(command=self.student_table.yview)
        #define table columns
        self.student_table['columns'] = ('Student No', 'Last Name', 'First Name','Middle Name', 'Subject Code')
        #format columns
        self.student_table.column('#0', width=0, stretch=0)
        self.student_table.column('Student No', anchor=CENTER, width=100)
        self.student_table.column('Last Name', anchor=CENTER, width=180)
        self.student_table.column('First Name',anchor=CENTER, width=180)
        self.student_table.column('Middle Name',anchor=CENTER,width=180)
        self.student_table.column('Subject Code',anchor=CENTER,width=180)
        #Creating Headings
        self.student_table.heading("#0", text="",anchor=CENTER)
        self.student_table.heading("Student No", text="Student No", anchor=CENTER)
        self.student_table.heading("Last Name", text="Last Name", anchor=CENTER)
        self.student_table.heading("First Name", text="First Name", anchor=CENTER)
        self.student_table.heading("Middle Name", text="Middle Name", anchor=CENTER)
        self.student_table.heading("Subject Code", text="Subject Code", anchor=CENTER)
        self.window.mainloop()  


    #----------------------------Method to get selected value from the listbox------------------------------------
    def getSelect(self,event):
        self.student_table.delete(*self.student_table.get_children())
        selection = event.widget.curselection()
        index = selection[0]
        slectedValue = event.widget.get(index)
        table_data = "SELECT student.student_no, student.last_name, student.first_name, student.middle_name, class.subject_code \
                    FROM student JOIN student_subjects ON student.id = student_subjects.student_id JOIN class ON class.id = student_subjects.subject_id \
                    WHERE subject_code LIKE '%"+slectedValue+"%' ORDER BY student.last_name ASC"
        dbcursor.execute(table_data)
        tDatas = dbcursor.fetchall()
        #loop tru tuple of data
        for data in tDatas:
            self.student_table.insert("", 'end',iid=data[0], text=data[0],values=(data[0], data[1], data[2], data[3], data[4]))

    #------------------------------Method to add subject----------------------------------------------------
    def add(self):
        subj_code = self.subj_code_entrybox.get().upper()
        subj_name = self.subj_name_entrybox.get().upper()
        crse_yr_sec = self.crse_yr_sec_entrybox.get().upper()
        #query database
        if len(subj_code) == 0 or len(subj_name) == 0 or len(crse_yr_sec) == 0:
            messagebox.showerror("ERROR", message="Please complete the info. fields")
        else:
            class_info = "INSERT INTO class(subject_code, subject_name, section ) VALUES (%s, %s, %s)"
            dbcursor.execute(class_info,(subj_code, subj_name, crse_yr_sec))
            db.commit()
            db.close()
        #Delete entries after being save
        self.subj_code_entrybox.delete(0, END)
        self.subj_name_entrybox.delete(0, END)
        self.crse_yr_sec_entrybox.delete(0,END)
    #------------------------------Method to remove subject----------------------------------------------
    def remove(self):
        try:
            subj_code = self.subj_id_entrybox.get().upper()
            # dbcursor.execute("SELECT * FROM class WHERE id ="+ subj_id)
            # subj_to_del = dbcursor.fetchone()
            #query database
            if len(subj_code) == 0:
                messagebox.showerror("Error", "Oops, enter subject id.")
            # elif subj_code not in self.listbox_value:
            #     messagebox.showerror("ERROR","Record not available.")
            else:
                delete_quer = f"DELETE FROM class WHERE subject_code = '{subj_code}'"
                dbcursor.execute(delete_quer)
                db.commit()
                db.close()
        except Exception:
            messagebox.showerror("ERROR","Refresh the page first")

        # delete entry in entrybox
        self.subj_id_entrybox.delete(0, END)
    #method for back button
    def back(self):
        self.window.destroy()
        os.system('py main_window.py')    
        
if __name__ == "__main__":        
    Class_Info(tk.Tk(),"CLASS INFORMATION")

