from datetime import datetime
from tkinter import*
from PIL import Image,ImageTk
from student import Student
from facerecognition import FaceRecognition
from attendance import Attendance
import os
import pandas as pd
import cv2
import numpy as np
from tkinter import messagebox

class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face_Recognition_System")
        self.root.resizable(False, False)  # Disable window resizing
        self.bg_images = [r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\homebg.jpg",
                          r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\homebg1.jpg",
                          r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\homebg2.jpg"]
        self.current_bg_index = 0
           # Define bg_img as a class variable
        self.bg_img = Label(self.root, image=None)  # Initialize with None or a default image
        self.bg_img.place(x=0, y=0, width=1366, height=758)
        self.change_background()
        self.root.resizable(False, False)  # Disable window resizing

    def change_background(self):
        if self.current_bg_index < len(self.bg_images) - 1:
            self.current_bg_index += 1
        else:
            self.current_bg_index = 0

        bg_image = Image.open(self.bg_images[self.current_bg_index])
        bg_image = bg_image.resize((1366, 768), Image.Resampling.LANCZOS)
        self.photobg = ImageTk.PhotoImage(bg_image)
        self.bg_img.config(image=self.photobg)
        self.bg_img.image = self.photobg

        self.root.after(5000, self.change_background)  # Change background every 5 seconds

        # set image as lable
        bg_img = Label(self.root,image=self.photobg)
        bg_img.place(x=0,y=0,width=1366,height=758)


        # #title section
        # title_lb1 = Label(bg_img,text="Attendance Managment System Using Facial Recognition",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        # title_lb1.place(x=0,y=0,width=1366,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # Create a common function for button hover
        def on_hover(event, button, color):
            button.config(bg=color)

        # Create a common function for button leave
        def on_leave(event, button, color):
            button.config(bg=color)

        # Student button 1
        std_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\std1.jpg")
        std_img_btn = std_img_btn.resize((90, 80), Image.Resampling.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.student_pannels, image=self.std_img1, cursor="hand2")
        std_b1.place(x=20, y=115, width=90, height=80)
        
        std_b1.bind("<Enter>", lambda event, button=std_b1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        std_b1.bind("<Leave>", lambda event, button=std_b1: on_leave(event, button, "white"))

        std_b1_1 = Button(bg_img, command=self.student_pannels, text="Student Panel", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=105, y=115, width=220, height=80)
        std_b1_1.bind("<Enter>", lambda event, button=std_b1_1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        std_b1_1.bind("<Leave>", lambda event, button=std_b1_1: on_leave(event, button, "white"))

        
        # Detect Face button 2
        det_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\det1.jpg")
        det_img_btn = det_img_btn.resize((90, 80), Image.Resampling.LANCZOS)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img, command=self.face_rec, image=self.det_img1, cursor="hand2")
        det_b1.place(x=20, y=210, width=90, height=80)
        det_b1.bind("<Enter>", lambda event, button=det_b1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        det_b1.bind("<Leave>", lambda event, button=det_b1: on_leave(event, button, "white"))

        det_b1_1 = Button(bg_img, command=self.face_rec, text="Take Attendance", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        det_b1_1.place(x=105, y=210, width=220, height=80)
        det_b1_1.bind("<Enter>", lambda event, button=det_b1_1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        det_b1_1.bind("<Leave>", lambda event, button=det_b1_1: on_leave(event, button, "white"))

         
        # Attendance System button 3
        att_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\att.jpg")
        att_img_btn = att_img_btn.resize((90, 80), Image.Resampling.LANCZOS)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img, command=self.attendance_pannel, image=self.att_img1, cursor="hand2")
        att_b1.place(x=20, y=305, width=90, height=80)
        att_b1.bind("<Enter>", lambda event, button=att_b1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        att_b1.bind("<Leave>", lambda event, button=att_b1: on_leave(event, button, "white"))

        att_b1_1 = Button(bg_img, command=self.attendance_pannel, text="View Attendance", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        att_b1_1.place(x=105, y=305, width=220, height=80)
        att_b1_1.bind("<Enter>", lambda event, button=att_b1_1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        att_b1_1.bind("<Leave>", lambda event, button=att_b1_1: on_leave(event, button, "white"))

        # Help Support button 4
        hlp_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\hlp.jpg")
        hlp_img_btn = hlp_img_btn.resize((90, 80), Image.Resampling.LANCZOS)
        self.hlp_img1 = ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(bg_img, command=self.helpSupport, image=self.hlp_img1, cursor="hand2")
        hlp_b1.place(x=20, y=600, width=90, height=80)
        hlp_b1.bind("<Enter>", lambda event, button=hlp_b1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        hlp_b1.bind("<Leave>", lambda event, button=hlp_b1: on_leave(event, button, "white"))

        hlp_b1_1 = Button(bg_img, command=self.helpSupport, text="Monthly Summary", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        hlp_b1_1.place(x=105, y=600, width=220, height=80)
        hlp_b1_1.bind("<Enter>", lambda event, button=hlp_b1_1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        hlp_b1_1.bind("<Leave>", lambda event, button=hlp_b1_1: on_leave(event, button, "white"))

        # Train button 5
        tra_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\tra1.jpg")
        tra_img_btn = tra_img_btn.resize((90, 80), Image.Resampling.LANCZOS)
        self.tra_img1 = ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(bg_img, command=self.train_pannels, image=self.tra_img1, cursor="hand2")
        tra_b1.place(x=20, y=400, width=90, height=80)
        tra_b1.bind("<Enter>", lambda event, button=tra_b1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        tra_b1.bind("<Leave>", lambda event, button=tra_b1: on_leave(event, button, "white"))

        tra_b1_1 = Button(bg_img, command=self.train_pannels, text="Data Train", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        tra_b1_1.place(x=105, y=400, width=220, height=80)
        tra_b1_1.bind("<Enter>", lambda event, button=tra_b1_1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        tra_b1_1.bind("<Leave>", lambda event, button=tra_b1_1: on_leave(event, button, "white"))

          # Photo button 6
        pho_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\qr1.png")
        pho_img_btn = pho_img_btn.resize((90, 80), Image.Resampling.LANCZOS)
        self.pho_img1 = ImageTk.PhotoImage(pho_img_btn)

        pho_b1 = Button(bg_img, command=self.open_img, image=self.pho_img1, cursor="hand2")
        pho_b1.place(x=20, y=500, width=90, height=80)
        pho_b1.bind("<Enter>", lambda event, button=pho_b1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        pho_b1.bind("<Leave>", lambda event, button=pho_b1: on_leave(event, button, "white"))

        pho_b1_1 = Button(bg_img, command=self.open_img, text="Data Set", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        pho_b1_1.place(x=105, y=500, width=220, height=80)
        pho_b1_1.bind("<Enter>", lambda event, button=pho_b1_1: on_hover(event, button, "#dee81c"))  # Change to your desired color
        pho_b1_1.bind("<Leave>", lambda event, button=pho_b1_1: on_leave(event, button, "white"))

        # # Developers   button 7
        # dev_img_btn=Image.open("/home/sakib/Desktop/Python_Test_Project/Images_GUI/dev.jpg")
        # dev_img_btn=dev_img_btn.resize((180,180),Image.ANTIALIAS)
        # self.dev_img1=ImageTk.PhotoImage(dev_img_btn)

        # dev_b1 = Button(bg_img,command=self.developr,image=self.dev_img1,cursor="hand2",)
        # dev_b1.place(x=710,y=330,width=180,height=180)

        # dev_b1_1 = Button(bg_img,command=self.developr,text="Developers",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        # dev_b1_1.place(x=710,y=510,width=180,height=45)

          # Exit button 8
        exi_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\exi.jpg")
        exi_img_btn = exi_img_btn.resize((90, 50), Image.Resampling.LANCZOS)
        self.exi_img1 = ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(bg_img, command=self.Close, image=self.exi_img1, cursor="hand2")
        exi_b1.place(x=20, y=700, width=90, height=50)
        exi_b1.bind("<Enter>", lambda event, button=exi_b1: on_hover(event, button, "red"))  # Change to your desired color
        exi_b1.bind("<Leave>", lambda event, button=exi_b1: on_leave(event, button, "White"))

        exi_b1_1 = Button(bg_img, command=self.Close, text="Exit", cursor="hand2",
                          font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        exi_b1_1.place(x=105, y=700, width=220, height=50)
        exi_b1_1.bind("<Enter>", lambda event, button=exi_b1_1: on_hover(event, button, "red"))  # Change to your desired color
        exi_b1_1.bind("<Leave>", lambda event, button=exi_b1_1: on_leave(event, button, "White"))

# ==================Funtion for Open Images Folder==================
    def open_img(self):
        file_path = r"C:\Users\dell\Desktop\Python_Test_Project\data_img" 
        
        try:
            os.startfile(file_path)
        except Exception as e:
            print(f"Error: {e}")
# ==================Functions Buttons=====================
    def student_pannels(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def train_pannels(self):
        data_dir=("data_img")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]
        
        faces=[]
        ids=[]

        for image in path:
            img=Image.open(image).convert('L') # conver in gray scale 
            imageNp = np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)

            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        
        ids=np.array(ids)
        
        #=================Train Classifier=============
        clf= cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("clf.xml")

        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training Dataset Complated!",parent=self.root)


    def face_rec(self):
        self.new_window=Toplevel(self.root)
        self.app=FaceRecognition(self.new_window)
    
    def attendance_pannel(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)
    
    # def developr(self):
    #     self.new_window=Toplevel(self.root)
    #     self.app=Developer(self.new_window)
    
    def helpSupport(self):
        
        today_date = datetime.now()
        month, year = today_date.strftime("%m"), today_date.strftime("%Y")
        folder_path = "Attendance_sheet"
        summary_filename = f"{folder_path}/attendance_summary_{month}_{year}.xlsx"

        if os.path.exists(summary_filename):
            df_summary = pd.read_excel(summary_filename)
        else:
            df_summary = pd.DataFrame(columns=['ID', 'Roll Number', 'Name'])

        total_days = 0

        for day in range(1, 32):  # Assuming max 31 days in a month
            day_str = f"{day:02d}"
            day_filename = os.path.join(folder_path, f"attendance_{day_str}-{month}-{year}.xlsx")  # Update path

            if os.path.exists(day_filename):
                day_df = pd.read_excel(day_filename)
                if not day_df.empty:  # Only consider days when attendance was taken
                    total_days += 1
                    for index, row in day_df.iterrows():
                        if row['ID'] != 'example_id':  # Exclude the example entry
                            student_id = row['ID']
                            student_roll_number = row['Roll Number']
                            student_name = row['Name']
                            student_status = row['Status']

                            student_entry = df_summary[(df_summary['ID'] == student_id) &
                                                    (df_summary['Roll Number'] == student_roll_number) &
                                                    (df_summary['Name'] == student_name)]

                            if student_entry.empty:
                                new_entry = {'ID': student_id, 'Roll Number': student_roll_number, 'Name': student_name}
                                new_entry[day_str] = student_status
                                df_summary = pd.concat([df_summary, pd.DataFrame([new_entry])], ignore_index=True)
                            else:
                                df_summary.loc[student_entry.index, day_str] = student_status

        # After collecting attendance data, calculate presence percentage
        for index, row in df_summary.iterrows():
            total_present = sum(1 for day in range(1, 32) if row.get(f"{day:02d}") == "Present")
            presence_percentage = (total_present / total_days) * 100
            df_summary.at[index, 'Presence Percentage'] = presence_percentage

        # Reorder columns so that 'Presence Percentage' is the last column
        day_columns = [col for col in df_summary.columns if col.isdigit()]
        column_order = ['ID', 'Roll Number', 'Name'] + ['Presence Percentage'] + day_columns
        df_summary = df_summary[column_order]

        try:
            df_summary.to_excel(summary_filename, index=False)
            # Display a success message
            messagebox.showinfo("Success", "Monthly summary generated successfully!", parent=self.root)
        except Exception as e:
            # Display an error message if there's an issue with saving the summary
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
   
   
    def Close(self):
        root.destroy()
    
        
    

if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.mainloop()