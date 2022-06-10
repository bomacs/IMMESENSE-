import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import os
import mysql.connector as mysql

#connecting to database
db = mysql.connect(host='localhost',user='root',password='', database='face_recog_attendance_db')
dbcursor = db.cursor()
#---------------------------------------------------------------------------------

#buttons container
class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.config(bg="#808080")
        self.window.state("zoomed")

        option = {"padx":5, "pady":5, "fill": BOTH}
        #create the left_frame
        self.left_frame = tk.Frame(self.window, bg='#808080')
        self.left_frame.pack(side=LEFT, padx=(150,5),expand=True)
        #self.left_frame.pack_propagate(False)  
        self.start_attendance_bttn = Button(self.left_frame, text="Start Attendance", command=self.strt_attendance,width=20)
        self.start_attendance_bttn.pack(side=TOP,**option)
        self.class_info_bttn = Button(self.left_frame, text="Class Info", command=self.view_class_info, width=20)
        self.class_info_bttn.pack(side=TOP,**option)
        self.view_report_bttn = Button(self.left_frame, text="View Report", command=self.report_attendance, width=20)
        self.view_report_bttn.pack(side=TOP, **option)
        self.register_student_bttn = Button(self.left_frame, text="Register Student", command=self.register_student, width=20)
        self.register_student_bttn.pack(side=TOP, **option)
        self.remove_student_bttn = Button(self.left_frame, text="Remove Student", command=self.remove_student)
        self.remove_student_bttn.pack(side=TOP, **option)
        self.logout_bttn = Button(self.left_frame, text="Log out", command=self.logout)
        self.logout_bttn.pack(side=TOP, **option)
        #create the right frame
        self.right_frame = tk.Frame(self.window, bg='#808080',width=660, height=500)
        self.right_frame.pack(side=RIGHT, padx=(0,150), expand=True)
        self.right_frame.pack_propagate(False)
        #place the canvas in a frame 
        self.canvas = tk.Canvas(self.right_frame, width=645, height=485)
        self.canvas.pack()
        self.immesense_logo = ImageTk.PhotoImage(Image.open("images/immesense.png"))
        self.canvas.create_image(2, 1, anchor=NW, image=self.immesense_logo)
       
        # show window
        self.window.mainloop()
    #method to start attendance button
    def strt_attendance(self):
        self.window.destroy()
        os.system('py attendance_window.py')
    #method to view class info
    def view_class_info(self):
        self.window.destroy()
        os.system('py class_info_window.py')
    #method to attendance_report window
    def report_attendance(self):
        self.window.destroy()
        os.system('py attendance_report_window.py')
    #method to register student
    def register_student(self):
        self.window.destroy()
        os.system('py registration_window.py')
    #method to logout  
    def logout(self):
        self.window.destroy()
        os.system('py login_window.py')
#--------------------------------Creating TopLevel Window to remove studen-------------------------------        
    def remove_student(self):
        self.remove_student_window = Toplevel()
        self.remove_student_window.title("REMOVE MEMBER")
        self.remove_student_window.geometry("600x400")
        self.remove_student_window.config(bg='#a6a6a6')

        frame = tk.Frame(self.remove_student_window, background="#a6a6a6")
        frame.pack()
        #labels
        studentID_label = tk.Label(frame, text="Enter Student No.:",font=('Helvitica', 12, 'bold'), bg="#a6a6a6")
        studentID_label.grid(row=0, column=0, pady=(100,5))
        #entryboxes
        self.studentID_entrybx = tk.Entry(frame, width=30,)
        self.studentID_entrybx.grid(row=0, column=1, pady=(100,5))
        #buttons
        remove_button = tk.Button(frame, text="Remove", command = self.remove_stud, width=15)
        remove_button.grid(row=2, column=1, pady=(50,5))
        exit_button = tk.Button(frame, text="Exit", command = self.remove_student_window.destroy, width=15)
        exit_button.grid(row=3, column=1)
      
    def remove_stud(self):
        stud_no = self.studentID_entrybx.get()
        # quer = f"SELECT * FROM student WHERE student_no = {stud_no}"
        # dbcursor.execute(quer)
        # student_rec = dbcursor.fetchmany()
        # for rec in student_rec:
        #     print(rec)
        if os.path.exists("students_images/"+ stud_no +".jpg"): 
            try:
                os.remove("students_images/"+ stud_no +".jpg")
                del_query = f"DELETE FROM student WHERE student_no = '{stud_no}'"
                dbcursor.execute(del_query)
                db.commit()
                db.close()
            except Exception as e:
                messagebox.showerror("ERROR", e)
                self.remove_student_window.destroy()
                self.remove_student()
        else:
            messagebox.showerror("ERROR", message="Check your information provided...")
            self.remove_student_window.destroy()
            self.remove_student()
        # delete entry in entrybox
        self.studentID_entrybx.delete(0, END)


if __name__== "__main__":
    app = App(tk.Tk(), "IMMESENSE Face Resognition Attendance System")
   
   