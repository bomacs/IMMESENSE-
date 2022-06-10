import cv2
import face_recognition
from tkinter import messagebox
import mysql.connector as mysql
import numpy as np
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

#connecting to database
db = mysql.connect(host='localhost',user='root',password='', database='face_recog_attendance_db')  
dbcursor = db.cursor()

    
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)

        return encodeList  
def markAttendance(student_no,subject_code):
    subject_code = selected_subj_entry.get().upper()
        
    # subject_id
    quer_subject = f"SELECT ID from class where subject_code = '{subject_code}'"
    dbcursor.execute(quer_subject)
    subject_id = dbcursor.fetchone()[0]
    # get student_id from table student
    quer = f"select ID from student where student_no = '{student_no}'"
    dbcursor.execute(quer)
    stud_no = dbcursor.fetchone()
    query = f"SELECT * FROM attendance\
        WHERE student_id = '{stud_no[0]}' AND class_id = '{subject_id}' AND date(date_time_in) = date(NOW())"
    dbcursor.execute(query)
    query_data = dbcursor.fetchmany()

    if len(query_data) == 0:
        attendance_data = f" INSERT INTO attendance(student_id,class_id,date_time_in) \
            VALUES ('{stud_no[0]}','{subject_id}', NOW())"
        dbcursor.execute(attendance_data)
        db.commit()

# def get_selected(widget):
#     subjectCode = widget.get().upper()
#     return subjectCode
    

def start_attendance(widget):
    subjectCode = widget.get().upper()
    if len(subjectCode) == 0:
        messagebox.showerror("ERROR","Provide subject code.")
    else:
        # Student Images directory       
        path = 'C:/Environments/students_images'
        # list of images
        images = []
        classNames = []
        mylist = os.listdir(path)
        for cl in mylist:  
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])

        encoded_studImage = findEncodings(images)
        #------take pictures from webcam-------------
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        while True:
            success,img = cap.read()
            imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            # finding the face location and encodings of each image
            faces_in_frame = face_recognition.face_locations(imgS)
            encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
            # iterate trough all faces found in current frame
            # get the image face location in faces_in_frame
            # get the encoded face in encoded_faces
            for encoded_face, faceloc in zip(encoded_faces, faces_in_frame):
                matches = face_recognition.compare_faces(encoded_studImage, encoded_face)
                faceDist = face_recognition.face_distance(encoded_studImage, encoded_face)
                matchIndex = np.argmin(faceDist)
                if matches[matchIndex]:
                    name = classNames[matchIndex].lower()
                    y1,x2,y2,x1 = faceloc
                    # since we scaled down by 40 times
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
                    cv2.putText(img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)
                    cv2.putText(img,"End - press 'q'", (10,25), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                    markAttendance(name, subjectCode)
            cv2.imshow('webcam', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
def back():
    window.destroy()
    os.system('py main_window.py')

def quit_program():
    end_program = messagebox.askquestion("Exit Program", "Are you sure, you want to exit?")
    if end_program == 'yes':
        window.destroy()

if __name__ == "__main__": 
    window = tk.Tk()
    window.title("ATTENDANCE")
    window.config(bg="#808080")
    window.state("zoomed")
    #Creating frame and canvas for taking image
    right_frame = tk.Frame(window, width=800, height=600)
    right_frame.pack(side=RIGHT, padx=(25,120), pady=75)
    right_frame.pack_propagate(False)
    #Create frame and widgets on it
    widgets_frame = tk.Frame(window, background='#808080')
    widgets_frame.pack(side=LEFT, padx=(120,0), pady=75, anchor=NW)
    subject_label = tk.Label(widgets_frame, text="Subjects", font=('Helvitica', 12, 'bold'),background="#808080")
    subject_label.grid(row=0,column=0,sticky=NW)
    selected_subj = tk.Label(widgets_frame, text="Enter Subject:", font=('Helvitica', 12, 'bold'),background="#808080")
    selected_subj.grid(row=1,column=0)
    selected_subj_entry= tk.Entry(widgets_frame,width=20)
    selected_subj_entry.grid(row=1,column=1)
    # Getting data from database
    dbcursor.execute("SELECT subject_code FROM class")
    subjects = dbcursor.fetchall()
    subjectList = []
    for subject in subjects:
        subjectList.append(subject[0])
    #Creating Listbbox
    listbox_subjects = tk.Listbox(widgets_frame, height=len(subjects), selectmode=OFF)
    listbox_subjects.grid(row=0, column=1,pady=(0,5))
    #insert values to listbox
    for val in subjects:
        listbox_subjects.insert(END, val[0])

    strt_attendance_button = tk.Button(widgets_frame, text="Start Attendance", command= lambda:start_attendance(selected_subj_entry), width=15)
    strt_attendance_button.grid(row=1, column=1,  padx=(0,5), pady=(100,5))
    back_button = tk.Button(widgets_frame, text="Back", command=back, width=15)
    back_button.grid(row=2,column=1, pady=(0,5), padx=(0,5))
    quit_button = tk.Button(widgets_frame, text="Quit", command=quit_program , width=15)
    quit_button.grid(row=3, column=1, padx=(0,5))
    
    window.mainloop()


