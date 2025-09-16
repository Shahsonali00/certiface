import glob
from tkinter import* 
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageTk
import cv2
import mysql.connector
import os
import tkinter.messagebox as messagebox
import numpy as np
import pkg_resources
import pygame
import hashlib  # Added hashlib for encryption


haar=pkg_resources.resource_filename('cv2','data/haarcascade_frontalface_default.xml')

class Register:
    
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1366x768+0+0")
        self.root.resizable(False, False)  # Disable window resizing

        pygame.init()
        # ============ Variables =================
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_cnum=StringVar()
        self.var_user_name=StringVar()
        self.var_sec_question=StringVar()
        self.var_sa=StringVar()
        self.var_pwd=StringVar()
        self.var_cpwd=StringVar()
        self.var_check=IntVar()

          # Load the image and resize it
        image = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\bgReg.jpg")
        image = image.resize((1366, 768), Image.Resampling.LANCZOS)

        # Convert the image to a PhotoImage object
        self.bg = ImageTk.PhotoImage(image=image)

        lb1_bg=Label(self.root,image=self.bg)
        lb1_bg.place(x=0,y=0, relwidth=1,relheight=1)

        frame= Frame(self.root,bg="#F2F2F2")
        frame.place(x=100,y=80,width=900,height=580)
        

        get_str = Label(frame,text="Registration",font=("times new roman",30,"bold"),fg="#002B53",bg="#F2F2F2")
        get_str.place(x=350,y=130)

        #label1 
        fname =lb1= Label(frame,text="First Name:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        fname.place(x=100,y=200)

        #entry1 
        self.txtuser=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.txtuser.place(x=103,y=225,width=270)
            # messagebox.showinfo("Successfully","Successfully Register!")


        #label2 
        lname =lb1= Label(frame,text="Last Name:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        lname.place(x=100,y=270)

        #entry2 
        self.txtpwd=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.txtpwd.place(x=103,y=295,width=270)

        # ==================== section 2 -------- 2nd Columan===================

        #label1 
        cnum =lb1= Label(frame,text="Contact No:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        cnum.place(x=530,y=200)

        #entry1 
        self.txtuser=ttk.Entry(frame,textvariable=self.var_cnum,font=("times new roman",15,"bold"))
        self.txtuser.place(x=533,y=225,width=270)


        #label2 
        user_name =lb1= Label(frame,text="User Name:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        user_name.place(x=530,y=270)

        #entry2 
        self.txtpwd=ttk.Entry(frame,textvariable=self.var_user_name,font=("times new roman",15,"bold"))
        self.txtpwd.place(x=533,y=295,width=270)

        # ========================= Section 3 --- 1 Columan=================

        #label1 
        sec_question =lb1= Label(frame,text="Select Security Question:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        sec_question.place(x=100,y=350)

        #Combo Box1
        self.combo_security = ttk.Combobox(frame,textvariable=self.var_sec_question,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security["values"]=("Select","Your Nick Name","Your Favorite Book")
        self.combo_security.current(0)
        self.combo_security.place(x=103,y=375,width=270)


        #label2 
        sa =lb1= Label(frame,text="Security Answer:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        sa.place(x=100,y=420)

        #entry2 
        self.txtpwd=ttk.Entry(frame,textvariable=self.var_sa,font=("times new roman",15,"bold"))
        self.txtpwd.place(x=103,y=445,width=270)

        # ========================= Section 4-----Column 2=============================

        #label1 
        pwd =lb1= Label(frame,text="Password:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        pwd.place(x=530,y=350)

        #entry1 
        self.txtuser=ttk.Entry(frame,textvariable=self.var_pwd,font=("times new roman",15,"bold"))
        self.txtuser.place(x=533,y=375,width=270)


        #label2 
        cpwd =lb1= Label(frame,text="Confirm Password:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        cpwd.place(x=530,y=420)

        #entry2 
        self.txtpwd=ttk.Entry(frame,textvariable=self.var_cpwd,font=("times new roman",15,"bold"),show='*')
        self.txtpwd.place(x=533,y=445,width=270)

        # Checkbutton
        checkbtn = Checkbutton(frame,variable=self.var_check,text="I Agree the Terms & Conditions",font=("times new roman",13,"bold"),fg="#002B53",bg="#F2F2F2")
        checkbtn.place(x=100,y=480,width=270)


        # Creating Button Register
        loginbtn=Button(frame,command=self.reg,text="Register",font=("times new roman",15,"bold"),bd=0,relief=RIDGE,fg="#fff",bg="#002B53",activeforeground="white",activebackground="#007ACC")
        loginbtn.place(x=30,y=520,width=200,height=35)

         # Bind the Enter key to the login function
        root.bind('<Return>', self.reg)

    
        # Create a button to upload admin images
        upload_admin_button = Button(frame, text="Register with Face_ID", command=self.upload_admin_image,font=("times new roman",15,"bold"),bd=0,relief=RIDGE,fg="#fff",bg="#002B53",activeforeground="white",activebackground="#007ACC")
        upload_admin_button.place(x=250,y=520,width=200,height=35)

        #Creating Button Login
        loginbtn=Button(frame,text="Login Page",command=self.back,font=("times new roman",15,"bold"),bd=0,relief=RIDGE,fg="#fff",bg="#002B53",activeforeground="white",activebackground="#007ACC")
        loginbtn.place(x=470,y=520,width=200,height=35)
        
        delete_btn = Button(frame, text="Delete Admin", command=self.delete_user, font=("times new roman", 15, "bold"), bd=0, relief=RIDGE, fg="#fff", bg="#002B53", activeforeground="white", activebackground="#007ACC")
        delete_btn.place(x=690, y=520, width=200, height=35)


        # Load admin face images from the "Admindata_img" directory
        self.admin_images_path = "Admindata_img"

        # Create the folder if it doesn't exist
        if not os.path.exists(self.admin_images_path):
            os.makedirs(self.admin_images_path)


        # # self.video_capture = cv2.VideoCapture(0)  # Open webcam
        # # self.check_face()

    def back(self):
        self.root.destroy()


    def upload_admin_image(self):
        if (
            self.var_fname.get() == ""
            or self.var_lname.get() == ""
            or self.var_cnum.get() == ""
            or self.var_user_name.get() == ""
            or self.var_sec_question.get() == "Select"
            or self.var_sa.get() == ""
            or self.var_pwd.get() == ""
            or self.var_cpwd.get() == ""
        ):
            messagebox.showerror("Error", "All Fields Required!", parent=self.root)
        elif self.var_pwd.get() != self.var_cpwd.get():
            messagebox.showerror(
                "Error", "Please Enter Password & Confirm Password are the Same!", parent=self.root
            )
        elif self.var_check.get() == 0:
            messagebox.showerror("Error", "Please Check the Agree Terms and Conditions!", parent=self.root)
        elif not self.is_valid_phone_number():
            messagebox.showerror("Error", "Invalid Phone Number!", parent=self.root)
        elif not self.is_valid_password():
            messagebox.showerror(
                "Error",
                "Invalid Password! Password must contain at least one number, one character, and be greater than 6 characters.",
                parent=self.root,
            )
        else:
            try:
                conn = mysql.connector.connect(
                    username='root', password='pass', host='localhost', database='face_recognition', port=3306
                )
                mycursor = conn.cursor()
                query = "select * from regteach where user_name=%s"
                value = (self.var_user_name.get(),)
                mycursor.execute(query, value)
                row = mycursor.fetchone()
                if row is not None:
                    messagebox.showerror(
                        "Error", "User already exists, please try another username", parent=self.root
                    )
                else:
                    # Encrypt the security answer and password
                    hashed_sa = hashlib.sha256(self.var_sa.get().encode()).hexdigest()
                    hashed_pwd = hashlib.sha256(self.var_pwd.get().encode()).hexdigest()

                    mycursor.execute(
                "insert into regteach (fname, lname, cnum, user_name, sec_question, sa, pwd) values(%s,%s,%s,%s,%s,%s,%s)",
                (
                    self.var_fname.get(),
                    self.var_lname.get(),
                    self.var_cnum.get(),
                    self.var_user_name.get(),
                    self.var_sec_question.get(),
                    hashed_sa,
                    hashed_pwd,
                ),
            )

                    conn.commit()
                    conn.close()

                    face_classifier = cv2.CascadeClassifier(haar)

                    def face_cropped(img):
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                        for (x, y, w, h) in faces:
                            face_cropped = img[y: y + h, x: x + w]
                            return face_cropped

                    cap = cv2.VideoCapture(0)
                    img_id = 0
                    while True:
                        ret, my_frame = cap.read()
                        if face_cropped(my_frame) is not None:
                            img_id += 1
                            face = cv2.resize(face_cropped(my_frame), (300, 300))
                            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                            file_path = f"Admindata_img/reg.{self.var_user_name.get()}.{img_id}.jpg"
                            cv2.imwrite(file_path, face)
                            cv2.putText(
                                face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2
                            )
                            cv2.imshow("Capture Images", face)

                        if cv2.waitKey(1) == 13 or int(img_id) == 30:
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                    self.train_classifier()

                    messagebox.showinfo("Result", "Generating dataset completed!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)



    # ==================Create Function of Traing===================
    def train_classifier(self):
        data_dir = "Admindata_img"
        clf_filename = "clf_admin.xml"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        
        faces = []
        labels = []

        label_id_mapping = {}  # To map usernames to integer labels
        current_label_id = 0

        for image in path:
            img = Image.open(image).convert('L')
            image_np = np.array(img, 'uint8')
            username = os.path.split(image)[1].split('.')[1]

            # Map username to a unique integer label
            if username not in label_id_mapping:
                label_id_mapping[username] = current_label_id
                current_label_id += 1

            label = label_id_mapping[username]

            faces.append(image_np)
            labels.append(label)

        labels = np.array(labels)

        # Train Classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, labels)
        clf.write(clf_filename)

        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training Dataset Completed!", parent=self.root)


    def reg(self, event=None):
        if (
            self.var_fname.get() == ""
            or self.var_lname.get() == ""
            or self.var_cnum.get() == ""
            or self.var_user_name.get() == ""
            or self.var_sec_question.get() == "Select"
            or self.var_sa.get() == ""
            or self.var_pwd.get() == ""
            or self.var_cpwd.get() == ""
        ):
            messagebox.showerror("Error", "All Fields Required!", parent=self.root)
        elif self.var_pwd.get() != self.var_cpwd.get():
            messagebox.showerror(
                "Error", "Please Enter Password & Confirm Password are the Same!", parent=self.root
            )
        elif self.var_check.get() == 0:
            messagebox.showerror("Error", "Please Check the Agree Terms and Conditions!", parent=self.root)
        elif not self.is_valid_phone_number():
            messagebox.showerror("Error", "Invalid Phone Number!", parent=self.root)
        elif not self.is_valid_password():
            messagebox.showerror(
                "Error",
                "Invalid Password! Password must contain at least one number, one character, and be greater than 6 characters.",
                parent=self.root,
            )
        else:
            try:
                conn = mysql.connector.connect(
                    username='root', password='pass', host='localhost', database='face_recognition', port=3306
                )
                mycursor = conn.cursor()
                query = "select * from regteach where user_name=%s"
                value = (self.var_user_name.get(),)
                mycursor.execute(query, value)
                row = mycursor.fetchone()
                if row is not None:
                    messagebox.showerror(
                        "Error", "User already exists, please try another username", parent=self.root
                    )
                else:
                    # Encrypt the security answer and password
                    hashed_sa = hashlib.sha256(self.var_sa.get().encode()).hexdigest()
                    hashed_pwd = hashlib.sha256(self.var_pwd.get().encode()).hexdigest()

                    mycursor.execute(
                        "insert into regteach (fname, lname, cnum, user_name, sec_question, sa, pwd) values(%s,%s,%s,%s,%s,%s,%s)",
                        (
                            self.var_fname.get(),
                            self.var_lname.get(),
                            self.var_cnum.get(),
                            self.var_user_name.get(),
                            self.var_sec_question.get(),
                            hashed_sa,
                            hashed_pwd,
                        ),
                    )
                    conn.commit()
                    conn.close()
                    pygame.mixer.music.load("Registeredaudio.wav")
                    pygame.mixer.music.play()
                    messagebox.showinfo("Success", "Registered Successfully!", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def is_valid_phone_number(self):
        phone_number = self.var_cnum.get()
        return phone_number.isdigit() and len(phone_number) <= 15

    def is_valid_password(self):
        password = self.var_pwd.get()
        return any(char.isdigit() for char in password) and any(char.isalpha() for char in password) and len(password) > 6


    def delete_user(self):
        # Function to delete user data
        delete_frame = Toplevel(self.root)
        delete_frame.title("Delete User")

        # Labels and entry widgets for username and password
        lbl_username = Label(delete_frame, text="Username:", font=("times new roman", 15, "bold"))
        lbl_username.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        entry_username = Entry(delete_frame, font=("times new roman", 15, "bold"))
        entry_username.grid(row=0, column=1, padx=20, pady=10)

        lbl_password = Label(delete_frame, text="Password:", font=("times new roman", 15, "bold"))
        lbl_password.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        entry_password = Entry(delete_frame, show="*", font=("times new roman", 15, "bold"))
        entry_password.grid(row=1, column=1, padx=20, pady=10)

        btn_delete = Button(delete_frame, text="Delete", command=lambda: self.confirm_delete(entry_username.get(), entry_password.get(), delete_frame), font=("times new roman", 15, "bold"), bd=0, relief=RIDGE, fg="#fff", bg="#002B53", activeforeground="white", activebackground="#007ACC")
        btn_delete.grid(row=2, columnspan=2, pady=20)

    def confirm_delete(self, entered_username, entered_password, delete_frame):
        try:
            # Connect to the database
            conn = mysql.connector.connect(username='root', password='pass', host='localhost', database='face_recognition', port=3306)
            mycursor = conn.cursor()

            # Query to retrieve user data based on username
            query = "SELECT * FROM regteach WHERE user_name = %s"
            value = (entered_username,)
            mycursor.execute(query, value)
            row = mycursor.fetchone()

            if row is not None:
                # Get the hashed password from the database
                stored_hashed_pwd = row[6]  # Assuming the password hash is stored in the 6th column

                # Hash the entered password
                hashed_entered_pwd = hashlib.sha256(entered_password.encode()).hexdigest()

                # Compare the hashed passwords
                if hashed_entered_pwd == stored_hashed_pwd:
                    # Passwords match, proceed with deletion

                    # Get the user images path
                    user_images_path = os.path.join("Admindata_img", f"reg.{entered_username}.")

                    # Delete user images
                    for file_path in glob.glob(user_images_path + "*.jpg"):
                        os.remove(file_path)

                    # Delete user data from the database
                    delete_query = "DELETE FROM regteach WHERE user_name = %s"
                    delete_value = (entered_username,)
                    mycursor.execute(delete_query, delete_value)
                    conn.commit()
                    conn.close()

                    # Inform the user about successful deletion
                    messagebox.showinfo("Success", "User data and images deleted successfully! Wait for Image Training", parent=self.root)

                    # Retrain the classifier after deletion
                    self.train_classifier()

                    # Close the delete frame
                    delete_frame.destroy()
                else:
                    # Display an error message for invalid password
                    messagebox.showerror("Error", "Invalid password!", parent=delete_frame)
            else:
                # Display an error message for invalid username
                messagebox.showerror("Error", "Invalid username!", parent=delete_frame)
        except Exception as es:
            # Display an error message for any exception
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=delete_frame)


if __name__ == "__main__":
    root=Tk()
    app=Register(root)
    root.mainloop()