import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk as PIL_ImageTk, Image as PIL_Image
import os
import cv2
import mysql.connector as mysql

#connecting to database
db = mysql.connect(host='localhost',user='root',password='', database='face_recog_attendance_db')
dbcursor = db.cursor()

class Registration:
    def __init__(self, window, window_title):
        self.window = window 
        self.window.title(window_title)
        self.window.config(bg='#808080')
        self.window.state('zoomed')
        #Creating left frame and widgets
        self.left_frame = tk.Frame(self.window, bg='#808080')
        self.left_frame.pack(side=LEFT, padx=(180,10), pady=100, anchor=NW)
        self.left_frame.pack_propagate(False)
        self.id_label = tk.Label(self .left_frame, text='Student No.', font=('Helvitica', 12,'bold'), bg='#808080')
        self.id_label.grid(row=0, column=0, sticky=W, pady=5)
        self.fname_label = tk.Label(self.left_frame, text='First Name', font=('Helvitica', 12, 'bold'), bg='#808080')
        self.fname_label.grid(row=1, column=0, sticky=W, pady=5)
        self.mname_label = tk.Label(self.left_frame, text='Middle Name', font=('Helvitica', 12, 'bold'), bg='#808080')
        self.mname_label.grid(row=2, column=0, sticky=W, pady=5)
        self.lname_label = tk.Label(self.left_frame, text='Last Name', font=('Helvitica', 12, 'bold'), bg='#808080')
        self.lname_label.grid(row=3, column=0, sticky=W, pady=5)
        self.enrolled_subj_label = tk.Label(self.left_frame, text='Enrolled Subjects', font=('Helvitica', 12, 'bold'), bg='#808080')
        self.enrolled_subj_label.grid(row=4, column=0, sticky=NW, pady=5)
        #entryboxes
        self.id_entrybox = tk.Entry(self.left_frame,width=30)
        self.id_entrybox.grid(row=0, column=1, pady=5)
        self.fname_entrybox = tk.Entry(self.left_frame,width=30)
        self.fname_entrybox.grid(row=1, column=1, pady=5)
        self.mname_entrybox  = tk.Entry(self.left_frame,width=30)
        self.mname_entrybox.grid(row=2, column=1, pady=5)
        self.lname_entrybox = tk.Entry(self.left_frame,width=30)
        self.lname_entrybox.grid(row=3, column=1, pady=5)
        #connecting to database
        dbcursor.execute("SELECT subject_code FROM class")
        listbox_value = dbcursor.fetchall()
        #Listbbox
        self.listbox_subjects = tk.Listbox(self.left_frame, height=len(listbox_value), width=20, selectmode=MULTIPLE)
        self.listbox_subjects.grid(row=4, column=1, pady=5)
        #-------Insert value to listbox----------------
        for val in listbox_value:
            self.listbox_subjects.insert(END, val[0])
        #buttons
        self.take_pic_button = tk.Button(self.left_frame, text='Take Picture',command=self.take_picture,width=15)
        self.take_pic_button.grid(row=5, column=1, pady=(90,5))
        self.save_button = tk.Button(self.left_frame, text='Save', width=15, command=self.save_student_info)
        self.save_button.grid(row=6, column=1, pady=5)
        self.back_button = tk.Button(self.left_frame, text='Back', width=15, command=self.back)
        self.back_button.grid(row=7, column=1, pady=5)

        # open video source
        self.studentImage = ImageCapture(0)

        #Creating frame and canvas for taking picture
        self.cam_frame = tk.Frame(self.window, width=self.studentImage.width, height=self.studentImage.height)
        self.cam_canvas = tk.Canvas(self.cam_frame, width=self.studentImage.width, height=self.studentImage.height)
        self.cam_canvas.pack(fill=BOTH, expand=True)
        self.cam_frame.pack(side=RIGHT, padx=(0,200), pady=(100,100), anchor=NE)
        self.cam_frame.pack_propagate(False)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update() 

        self.window.mainloop()

    #method to update video
    def update(self):
        # get a frame from the video source
        return_value, frame = self.studentImage.get_frame()

        if return_value:
            self.photo = PIL_ImageTk.PhotoImage(image=PIL_Image.fromarray(frame))
            self.cam_canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.window.after(self.delay, self.update)
    #method to take a student image
    def take_picture(self):
        self.student_no = self.id_entrybox.get()
        last_name = self.lname_entrybox.get().title()
        first_name = self.fname_entrybox.get().title()
        middle_name = self.mname_entrybox.get().title()
        path = 'C:/Environments/students_images'
        # Connect to database
        student_info = f"INSERT INTO student(student_no, last_name, first_name, middle_name) VALUES ('{self.student_no}','{last_name}','{first_name}','{middle_name}')"
        dbcursor.execute(student_info)
        db.commit()
        if len(last_name) == 0 or len(first_name) == 0 or len(self.id_entrybox.get()) == 0:
            messagebox.showerror('ERROR','Please complete info fields.')
        else:
            try:
                return_value, frame = self.studentImage.get_frame()
                if return_value:
                    cv2.imwrite(os.path.join(path, self.student_no + ".jpg"), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    messagebox.showinfo("",'Image uploaded!!')
            except Exception as e:
                messagebox.showerror("",message="Error:" + (e))
        # stud_no = self.id_entrybox.get()
        # studID_quer = f"SELECT ID FROM student WHERE student_no = {stud_no}"
        # dbcursor.execute(studID_quer)
        # self.student_id = dbcursor.fetchone()[0]
    #------------------Method to save students subject ----------------------------------------- 
    def save_student_info(self):
        stud_subj = []
        stud_no = self.id_entrybox.get()
        studID_quer = f"SELECT ID FROM student WHERE student_no = '{stud_no}'"
        dbcursor.execute(studID_quer)
        student_id = dbcursor.fetchone()
        # student info to table student
        selectionSet = set()
        selection =  self.listbox_subjects.curselection()
        for val in selection:
            subject = self.listbox_subjects.get(val)
            selectionSet.add(subject)
    
        if len(selectionSet) == 0 or len(self.id_entrybox.get()) == 0:
            messagebox.showerror("ERROR", "Must complete fields and select your subjects.")
        else:
            try:
                for subj in selectionSet:
                    query_subj = f"SELECT ID FROM class WHERE subject_code = '{subj}'"
                    dbcursor.execute(query_subj)
                    subj_id = dbcursor.fetchone()
                    stud_subj.append(subj_id)
                for sub in stud_subj:
                    query = f"INSERT INTO student_subjects(student_id,subject_id) VALUES ({student_id[0]},{sub[0]})"
                    dbcursor.execute(query)
                    db.commit()
            except Exception:
                messagebox.showerror("ERROR", "Something went wrong")
            self.listbox_subjects.selection_clear(0, END)
        #Delete entries after being save
        self.id_entrybox.delete(0, END)
        self.lname_entrybox.delete(0, END)
        self.fname_entrybox.delete(0,END)
        self.mname_entrybox.delete(0,END)        
        
    #method for back button
    def back(self):
        self.studentImage.__del__()
        self.window.destroy()
        os.system('py main_window.py')
      
class ImageCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            return_value, frame = self.vid.read()
            if return_value:
                # Return a boolean success flag and the current frame converted to BGR
                return (return_value, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (return_value, None)

    # release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    Registration(tk.Tk(),"REGISTRATION")
