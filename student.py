import os
import re
from tkinter import* 
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import pkg_resources
from tkcalendar import Calendar  # Import the Calendar widget
from tkinter import Tk, Label, Entry, Button, Frame, Toplevel

haar=pkg_resources.resource_filename('cv2','data/haarcascade_frontalface_default.xml')


class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x883+0+0")
        self.root.title("Student Pannel")
        root.resizable(True,True)
        self.calendar_open = False  # Flag to track if calendar is open
        root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        #-----------Variables-------------------
        self.var_PU_Registration  = StringVar()
        self.var_std_name = StringVar()
        self.var_program = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_level = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_mob = StringVar()
        self.var_college_name = StringVar()
        self.var_exam_rollno = StringVar()
        self.var_email = StringVar()
        self.var_radio1 = StringVar()



         # backgorund image 
        bg1=Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\stdbg.jpg")
        bg1 = bg1.resize((1366, 883), Image.Resampling.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=0,width=1366,height=883)



        # Creating Frame 
        main_frame = Frame(bg_img,bd=2,bg="white") #bd mean border 
        main_frame.place(x=5,y=240,width=1355,height=600)

        # Left Label Frame 
        left_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("verdana",12,"bold"),fg="navyblue")
        left_frame.place(x=10,y=10,width=800,height=550)

        # Current Course 
        current_course_frame = LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,text="Current Course",font=("verdana",12,"bold"),fg="navyblue")
        current_course_frame.place(x=10,y=5,width=635,height=150)

        #label Program
        dep_label=Label(current_course_frame,text="Program ",font=("verdana",12,"bold"),bg="white",fg="navyblue")
        dep_label.grid(row=0,column=0,padx=5,pady=15)

        #combo box 
        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_program,width=15,font=("verdana",12,"bold"),state="readonly")
        dep_combo["values"]=("Select program ","BEcomputing","BEcivil","BeIT")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=5,pady=15,sticky=W)

        # -----------------------------------------------------

       
        #-------------------------------------------------------------

        #label Year
        year_label=Label(current_course_frame,text="Year",font=("verdana",12,"bold"),bg="white",fg="navyblue")
        year_label.grid(row=1,column=0,padx=5,sticky=W)

        #combo box 
        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_year,width=15,font=("verdana",12,"bold"),state="readonly")
        year_combo["values"]=("Select Admitted Year","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024,2025")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=5,pady=15,sticky=W)

        #-----------------------------------------------------------------

        #label Semester 
        year_label=Label(current_course_frame,text="Semester",font=("verdana",12,"bold"),bg="white",fg="navyblue")
        year_label.grid(row=1,column=2,padx=5,sticky=W)

        #combo box 
        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_semester,width=15,font=("verdana",12,"bold"),state="readonly")
        year_combo["values"]=("Select Semester","First","Second","Third","Fourth","Sixth","Seventh","Eighth")
        year_combo.current(0)
        year_combo.grid(row=1,column=3,padx=5,pady=15,sticky=W)

        #Class Student Information
        class_Student_frame = LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,text="Class Student Information",font=("verdana",12,"bold"),fg="navyblue")
        class_Student_frame.place(x=10,y=160,width=635,height=230)

        #Student id
        studentId_label = Label(class_Student_frame,text="PU_Registration",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        studentId_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)

        studentId_entry = ttk.Entry(class_Student_frame,textvariable=self.var_PU_Registration ,width=15,font=("verdana",12,"bold"))
        studentId_entry.grid(row=0,column=1,padx=5,pady=5,sticky=W)

        #Student name
        student_name_label = Label(class_Student_frame,text="Std-Name:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_name_label.grid(row=0,column=2,padx=5,pady=5,sticky=W)

        student_name_entry = ttk.Entry(class_Student_frame,textvariable=self.var_std_name,width=15,font=("verdana",12,"bold"))
        student_name_entry.grid(row=0,column=3,padx=5,pady=5,sticky=W)

        #Class Didvision
        student_div_label = Label(class_Student_frame,text="Class Timing:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_div_label.grid(row=1,column=0,padx=5,pady=5,sticky=W)

        div_combo=ttk.Combobox(class_Student_frame,textvariable=self.var_level,width=13,font=("verdana",12,"bold"),state="readonly")
        div_combo["values"]=("Morning","Evening")
        div_combo.current(0)
        div_combo.grid(row=1,column=1,padx=5,pady=5,sticky=W)

        #Roll No
        student_roll_label = Label(class_Student_frame,text="Exam_Roll-No:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_roll_label.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        student_roll_entry = ttk.Entry(class_Student_frame,textvariable=self.var_exam_rollno,width=15,font=("verdana",12,"bold"))
        student_roll_entry.grid(row=1,column=3,padx=5,pady=5,sticky=W)

        #Gender
        student_gender_label = Label(class_Student_frame,text="Gender:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_gender_label.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        #combo box 
        gender_combo=ttk.Combobox(class_Student_frame,textvariable=self.var_gender,width=13,font=("verdana",12,"bold"),state="readonly")
        gender_combo["values"]=("Male","Female","Others")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=5,pady=5,sticky=W)

        # Date of Birth
        student_dob_label = Label(class_Student_frame, text="DOB:", font=("verdana", 12, "bold"), fg="navyblue", bg="white")
        student_dob_label.grid(row=2, column=2, padx=5, pady=5, sticky=W)

        self.var_dob = StringVar()
        student_dob_entry = ttk.Entry(class_Student_frame, textvariable=self.var_dob, width=15, font=("verdana", 12, "bold"))
        student_dob_entry.grid(row=2, column=3, padx=5, pady=5, sticky=W)
        student_dob_entry.insert(0, "yy/mm/dd")  # Add a placeholder text
        self.cal = None  # Calendar widget instance
        student_dob_entry.bind("<Button-1>", self.open_calendar)




        #Email
        student_email_label = Label(class_Student_frame,text="Email:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_email_label.grid(row=3,column=0,padx=5,pady=5,sticky=W)

        student_email_entry = ttk.Entry(class_Student_frame,textvariable=self.var_email,width=15,font=("verdana",12,"bold"))
        student_email_entry.grid(row=3,column=1,padx=5,pady=5,sticky=W)

        #Phone Number
        student_mob_label = Label(class_Student_frame,text="Mob-No:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_mob_label.grid(row=3,column=2,padx=5,pady=5,sticky=W)

        student_mob_entry = ttk.Entry(class_Student_frame,textvariable=self.var_mob,width=15,font=("verdana",12,"bold"))
        student_mob_entry.grid(row=3,column=3,padx=5,pady=5,sticky=W)

        #College
        student_address_label = Label(class_Student_frame,text="College:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_address_label.grid(row=4,column=0,padx=5,pady=5,sticky=W)

        student_address_entry = ttk.Entry(class_Student_frame,textvariable=self.var_college_name,width=15,font=("verdana",12,"bold"))
        student_address_entry.grid(row=4,column=1,padx=5,pady=5,sticky=W)


        #Radio Buttons
        self.var_radio1=StringVar()
        radiobtn1=ttk.Radiobutton(class_Student_frame,text="Take Photo Sample",variable=self.var_radio1,value="Yes")
        radiobtn1.grid(row=5,column=0,padx=5,pady=5,sticky=W)

        radiobtn1=ttk.Radiobutton(class_Student_frame,text="No Photo Sample",variable=self.var_radio1,value="No")
        radiobtn1.grid(row=5,column=1,padx=5,pady=5,sticky=W)

        #Button Frame
        btn_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        btn_frame.place(x=10,y=390,width=635,height=60)

        #save button
        save_btn=Button(btn_frame,command=self.add_data,text="Save",width=7,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        save_btn.grid(row=0,column=0,padx=5,pady=10,sticky=W)

        #update button
        update_btn=Button(btn_frame,command=self.update_data,text="Update",width=7,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        update_btn.grid(row=0,column=1,padx=5,pady=8,sticky=W)

        #delete button
        del_btn=Button(btn_frame,command=self.delete_data,text="Delete",width=7,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        del_btn.grid(row=0,column=2,padx=5,pady=10,sticky=W)

        #reset button
        reset_btn=Button(btn_frame,command=self.reset_data,text="Reset",width=7,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        reset_btn.grid(row=0,column=3,padx=5,pady=10,sticky=W)

        #take photo button
        take_photo_btn=Button(btn_frame,command=self.generate_dataset,text="Take Pic",width=9,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        take_photo_btn.grid(row=0,column=4,padx=5,pady=10,sticky=W)

        #update photo button
        # update_photo_btn=Button(btn_frame,text="Update Pic",width=9,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        # update_photo_btn.grid(row=0,column=5,padx=5,pady=10,sticky=W)




        #----------------------------------------------------------------------
        # Right Label Frame 
        right_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("verdana",12,"bold"),fg="navyblue")
        right_frame.place(x=680,y=10,width=660,height=550)

        #Searching System in Right Label Frame 
        search_frame = LabelFrame(right_frame,bd=2,bg="white",relief=RIDGE,text="Search System",font=("verdana",12,"bold"),fg="navyblue")
        search_frame.place(x=10,y=5,width=635,height=80)

        #Phone Number
        search_label = Label(search_frame,text="Search:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        search_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.var_searchTX=StringVar()
        #combo box 
        search_combo=ttk.Combobox(search_frame,textvariable=self.var_searchTX,width=12,font=("verdana",12,"bold"),state="readonly")
        search_combo["values"] = ("Select", "Exam_RollNo", "PU_Registration")        
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=5,pady=15,sticky=W)

        self.var_search=StringVar()
        search_entry = ttk.Entry(search_frame,textvariable=self.var_search,width=12,font=("verdana",12,"bold"))
        search_entry.grid(row=0,column=2,padx=5,pady=5,sticky=W)

        search_btn=Button(search_frame,command=self.search_data,text="Search",width=9,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        search_btn.grid(row=0,column=3,padx=5,pady=10,sticky=W)

        showAll_btn=Button(search_frame,command=self.fetch_data,text="Show All",width=8,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        showAll_btn.grid(row=0,column=4,padx=5,pady=10,sticky=W)

        # -----------------------------Table Frame-------------------------------------------------
        #Table Frame 
        #Searching System in Right Label Frame 
        table_frame = Frame(right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=10,y=90,width=635,height=360)

        #scroll bar 
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        #create table 
        self.student_table = ttk.Treeview(table_frame, columns=("PU_Registration", "Name", "Program", "Year", "Semester", "Level", "Gender", "DOB", "Mobile_No", "CollegeName", "Exam_RollNo", "Email", "PhotoSample"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("PU_Registration", text="PU Registration")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Program", text="Program")
        self.student_table.heading("Year", text="Year")
        self.student_table.heading("Semester", text="Semester")
        self.student_table.heading("Level", text="Level")
        self.student_table.heading("Gender", text="Gender")
        self.student_table.heading("DOB", text="DOB")
        self.student_table.heading("Mobile_No", text="Mobile No")
        self.student_table.heading("CollegeName", text="College Name")
        self.student_table.heading("Exam_RollNo", text="Exam Roll No")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("PhotoSample", text="Photo Sample")
        self.student_table["show"] = "headings"


        # Set Width of Colums 
        self.student_table.column("PU_Registration", width=100)
        self.student_table.column("Name", width=100)
        self.student_table.column("Program", width=100)
        self.student_table.column("Year", width=100)
        self.student_table.column("Semester", width=100)
        self.student_table.column("Level", width=100)
        self.student_table.column("Gender", width=100)
        self.student_table.column("DOB", width=100)
        self.student_table.column("Mobile_No", width=100)
        self.student_table.column("CollegeName", width=100)
        self.student_table.column("Exam_RollNo", width=100)
        self.student_table.column("Email", width=100)
        self.student_table.column("PhotoSample", width=100)



        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
        self.fetch_data
# ==================Function Decleration==============================
    def add_data(self):
        if (
            self.var_program.get() == "Select Program"
            or self.var_year.get() == "Select Year"
            or self.var_semester.get() == "Select Semester"
            or self.var_PU_Registration .get() == ""
            or self.var_std_name.get() == ""
            or self.var_level.get() == ""
            or self.var_exam_rollno.get() == ""
            or self.var_gender.get() == ""
            or self.var_dob.get() == ""
            or self.var_mob.get() == ""
            or self.var_college_name.get() == ""
        ):
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
        else:
            # Validate the email address using a regular expression
            email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
            if not re.match(email_regex, self.var_email.get()):
                messagebox.showerror("Error", "Invalid Email Address", parent=self.root)
            else:
                try:
                    conn = mysql.connector.connect(
                        username="root",
                        password="pass",
                        host="localhost",
                        database="face_recognition",
                        port=3306,
                    )
                    mycursor = conn.cursor()
                    mycursor.execute(
                        "insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (
                            self.var_PU_Registration.get(),
                            self.var_std_name.get(),
                            self.var_program.get(),
                            self.var_year.get(),
                            self.var_semester.get(),
                            self.var_level.get(),
                            self.var_gender.get(),
                            self.var_dob.get(),
                            self.var_mob.get(),
                            self.var_college_name.get(),
                            self.var_exam_rollno.get(),
                            self.var_email.get(),
                            self.var_radio1.get(),
                        ),
                    )

                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "All Records are Saved!", parent=self.root)
                except Exception as es:
                    messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)


    # ===========================Fetch data form database to table ================================

    def fetch_data(self):
        conn = mysql.connector.connect(username='root', password='pass',host='localhost',database='face_recognition',port=3306)
        mycursor = conn.cursor()

        mycursor.execute("select * from student")
        data=mycursor.fetchall()

        if len(data)!= 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    #================================get cursor function=======================

    def get_cursor(self,event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_PU_Registration.set(data[0]),
        self.var_std_name.set(data[1]),
        self.var_program.set(data[2]),
       # self.var_course.set(data[3]),
        self.var_year.set(data[3]),
        self.var_semester.set(data[4]),
        self.var_level.set(data[5]),
        self.var_gender.set(data[6]),
        self.var_dob.set(data[7]),
        self.var_mob.set(data[8]),
        self.var_college_name.set(data[9]),
        self.var_exam_rollno.set(data[10]),
        self.var_email.set(data[11]),
        #self.var_teacher.set(data[13]),
        self.var_radio1.set(data[12])
    # ========================================Update Function==========================
        
    def update_data(self):
        if (
            self.var_program.get() == "Select Program"
            or self.var_year.get() == "Select Year"
            or self.var_semester.get() == "Select Semester"
            or self.var_PU_Registration.get() == ""
            or self.var_std_name.get() == ""
            or self.var_level.get() == ""
            or self.var_exam_rollno.get() == ""
            or self.var_gender.get() == ""
            or self.var_dob.get() == ""
            or self.var_email.get() == ""
            or self.var_mob.get() == ""
            or self.var_college_name.get() == ""
        ):
            messagebox.showerror("Error", "Please Fill All Fields are Required!", parent=self.root)
            return

        # Email validation using regular expression
        email_pattern = r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
        if not re.match(email_pattern, self.var_email.get()):
            messagebox.showerror("Error", "Invalid Email Format", parent=self.root)
            return

        try:
            update = messagebox.askyesno("Update", "Do you want to update this student’s details?", parent=self.root)
            if update:
                conn = mysql.connector.connect(
                    username='root',
                    password='pass',
                    host='localhost',
                    database='face_recognition',
                    port=3306
                )
                mycursor = conn.cursor()
                mycursor.execute(
                    """
                    UPDATE student
                    SET Name=%s, Program=%s, Year=%s, Semester=%s, Level=%s, Gender=%s, DOB=%s, Mobile_No=%s, CollegeName=%s, Email=%s, PhotoSample=%s
                    WHERE Exam_RollNo=%s
                    """,
                    (
                        self.var_std_name.get(),
                        self.var_program.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_level.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_mob.get(),
                        self.var_college_name.get(),
                        self.var_email.get(),
                        self.var_radio1.get(),
                        self.var_exam_rollno.get()
                    )
                )
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Successfully Updated!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
    #==============================Delete Function=========================================
        
    def delete_data(self):
        if self.var_exam_rollno.get() == "":
            messagebox.showerror("Error", "Exam_RollNo Must be Required!", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Do you want to Delete?", parent=self.root)
                if delete > 0:
                    # Delete all image files associated with the student
                    Exam_RollNo = self.var_exam_rollno.get()
                    for i in range(1, 101):
                        img_path = f"data_img/student.{Exam_RollNo}.{i}.jpg"
                        print(f"Deleting image file: {img_path}")
                        try:
                            os.remove(img_path)
                            print(f"Deleted successfully!")
                        except FileNotFoundError:
                            print("File not found.")
                        except Exception as e:
                            print(f"Error deleting image file: {str(e)}")

                    conn = mysql.connector.connect(username='root', password='pass', host='localhost',
                                                database='face_recognition', port=3306)
                    mycursor = conn.cursor()
                    sql = "delete from student where Exam_RollNo=%s"
                    val = (Exam_RollNo,)
                    mycursor.execute(sql, val)
                else:
                    if not delete:
                        return

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete", "Successfully Deleted!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
            
    # Reset Function 
    def reset_data(self):
        self.var_PU_Registration.set(""),
        self.var_std_name.set(""),
        self.var_program.set("Select Program"),
      #  self.var_course.set("Select Course"),
        self.var_year.set("Select Year"),
        self.var_semester.set("Select Semester"),
        self.var_level.set("Morning"),
        self.var_gender.set("Male"),
        self.var_dob.set(""),
        self.var_mob.set(""),
        self.var_college_name.set(""),
        self.var_exam_rollno.set(""),
        self.var_email.set(""),
       # self.var_teacher.set(""),
        self.var_radio1.set("")
    
    # ===========================Search Data===================
    def search_data(self):
        if self.var_search.get() == "" or self.var_searchTX.get() == "Select":
            messagebox.showerror("Error", "Select Combo option and enter entry box", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(username='root', password='pass', host='localhost', database='face_recognition', port=3306)
                my_cursor = conn.cursor()
                
                search_option = self.var_searchTX.get()
                search_value = self.var_search.get()
                
                if search_option == "Exam_RollNo":
                    sql = "SELECT PU_Registration , Name, Program, Year, Semester, Level, Gender, DOB, Mobile_No, CollegeName, Exam_RollNo, Email, PhotoSample FROM student WHERE Exam_RollNo='" + str(search_value) + "'"
                elif search_option == "PU_Registration":
                    sql = "SELECT PU_Registration , Name, Program, Year, Semester, Level, Gender, DOB, Mobile_No, CollegeName, Exam_RollNo, Email, PhotoSample FROM student WHERE PU_Registration='" + str(search_value) + "'"
                
                my_cursor.execute(sql)
                rows = my_cursor.fetchall()
                
                if len(rows) != 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in rows:
                        self.student_table.insert("", END, values=i)
                else:
                    messagebox.showerror("Error", "Data Not Found", parent=self.root)
                
                conn.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To : {str(es)}", parent=self.root)



#=====================This part is related to Opencv Camera part=======================
# ==================================Generate Data set take image=========================
    def generate_dataset(self):
        if self.var_program.get()=="Select Program" or self.var_year.get()=="Select Year" or self.var_semester.get()=="Select Semester" or self.var_PU_Registration.get()=="" or self.var_std_name.get()=="" or self.var_level.get()=="" or self.var_exam_rollno.get()=="" or self.var_gender.get()=="" or self.var_dob.get()=="" or self.var_email.get()=="" or self.var_mob.get()=="" or self.var_college_name.get()=="":
            messagebox.showerror("Error","Please Fill All Fields are Required!",parent=self.root)
        else:
            try:
                
                conn = mysql.connector.connect(username='root', password='pass',host='localhost',database='face_recognition',port=3306)
                mycursor = conn.cursor()
                mycursor.execute("select * from student")
                myreslut = mycursor.fetchall()
                id = self.var_exam_rollno.get()


                mycursor.execute("update student set Name=%s,Program=%s,Year=%s,Semester=%s,Level=%s,Gender=%s,DOB=%s,Mobile_No=%s,CollegeName=%s,PU_Registration=%s,Email=%s,PhotoSample=%s where Exam_RollNo=%s",( 
                    self.var_std_name.get(),
                                        self.var_program.get(),
                                        self.var_year.get(),
                                        self.var_semester.get(),
                                        self.var_level.get(),
                                        self.var_gender.get(),
                                        self.var_dob.get(),
                                        self.var_mob.get(),
                                        self.var_college_name.get(),
                                        self.var_PU_Registration.get(),
                                        self.var_email.get(),
                                        self.var_radio1.get(),
                                        
                    id   
                    ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                # ====================part of opencv=======================

                face_classifier = cv2.CascadeClassifier(haar)

                def face_croped(img):
                    # conver gary sacle
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray,1.3,5)
                    #Scaling factor 1.3
                    # Minimum naber 5
                    for (x,y,w,h) in faces:
                        face_croped=img[y:y+h,x:x+w]
                        return face_croped
                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    ret,my_frame=cap.read()
                    if face_croped(my_frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_croped(my_frame),(300,300))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_path="data_img/student."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)        
                        cv2.imshow("Capture Images",face)

                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Generating dataset completed!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root) 
            
   

    def open_calendar(self, event=None):
        if not self.calendar_open:  # Check if calendar is already open
            self.top = Toplevel()
            self.cal = Calendar(self.top, date_pattern="yyyy/mm/dd")
            self.cal.pack(fill="both", expand=True)
            self.cal.bind("<<CalendarSelected>>", self.update_dob_entry)
            self.top.protocol("WM_DELETE_WINDOW", self.on_calendar_close)  # Handle window close event
            self.calendar_open = True  # Set flag to indicate calendar is open

    def update_dob_entry(self, event):
        selected_date = event.widget.get_date()
        self.var_dob.set(selected_date)
        self.top.destroy()  # Close the calendar window
        self.calendar_open = False  # Reset flag as calendar is closed

    def on_calendar_close(self):
        self.calendar_open = False  # Reset flag as calendar is manually closed
        self.top.destroy()
    
        
    def on_window_close(self):
        if self.calendar_open:
            self.on_calendar_close()  # Close the calendar if it is open
        self.root.destroy()  # Close the main window
        

# main class object

if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()
