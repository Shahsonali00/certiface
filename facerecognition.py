import os
import time
import cv2
import pandas as pd
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import tkinter.messagebox as messagebox
import pygame


class FaceRecognition:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Panel")
        pygame.init()
        self.root.resizable(False, False)

        bg1 = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\fd.jpg")
        bg1 = bg1.resize((1366, 768), Image.Resampling.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=0, width=1366, height=768)

        std_img_btn = Image.open(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\gate.png")
        std_img_btn = std_img_btn.resize((240, 200), Image.Resampling.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        self.gate_img_button = Button(bg_img, command=self.face_recog, image=self.std_img1, cursor="hand2")
        self.gate_img_button.place(x=550, y=250, width=250, height=200)

        self.gate_text_button = Button(bg_img, command=self.face_recog, text="Exam Attendance", cursor="hand2",
                                      font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        self.gate_text_button.place(x=550, y=450, width=250, height=45)

        self.clock_label = Label(root, font=('calibri', 20, 'bold'), background='black', foreground='white')
        self.clock_label.pack(anchor='se', padx=38, pady=140)

        self.update_clock()

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S %p')
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def is_attendance_marked(self, Exam_RollNo, student_name):
        today_date = datetime.now().strftime("%d-%m-%Y")
        folder_path = "Attendance_sheet"
        filename = f"{folder_path}/attendance_{today_date}.xlsx"

        if os.path.exists(filename):
            df = pd.read_excel(filename)
            return (df['Exam_RollNo'] == Exam_RollNo).any() or (df['Name'] == student_name).any()
        else:
            return False

    def mark_attend(self, i, r, n):
        today_datetime = datetime.now()
        today_date = today_datetime.strftime("%d-%m-%Y")
        today_time = today_datetime.strftime("%H:%M:%S")

        folder_path = "Attendance_sheet"
        filename = f"{folder_path}/attendance_{today_date}.xlsx"

        pygame.mixer.music.load("Attendance marked.wav")

        if os.path.exists(filename):
            df = pd.read_excel(filename)
            if (df['Exam_RollNo'] == i).any() or (df['Name'] == n).any():
                print("Attendance already marked for this person today.")
                return
        else:
            df = pd.DataFrame()

        pygame.mixer.music.play()

        new_entry = {'Exam_RollNo': i, 'PU_Registration': r, 'Name': n, 'Date': today_date,
                     'Time': today_time, 'Status': "Present"}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(filename, index=False)

    def generate_monthly_summary(self):
        today_date = datetime.now()
        month, year = today_date.strftime("%m"), today_date.strftime("%Y")
        folder_path = "Attendance_sheet"
        summary_filename = f"{folder_path}/attendance_summary_{month}_{year}.xlsx"

        if os.path.exists(summary_filename):
            df_summary = pd.read_excel(summary_filename)
        else:
            df_summary = pd.DataFrame(columns=['Exam_RollNo', 'PU_Registration', 'Name'])

        total_days = 0

        for day in range(1, 32):
            day_str = f"{day:02d}"
            day_filename = os.path.join(folder_path, f"attendance_{day_str}-{month}-{year}.xlsx")

            if os.path.exists(day_filename):
                day_df = pd.read_excel(day_filename)
                if not day_df.empty:
                    total_days += 1
                    for index, row in day_df.iterrows():
                        if row['Exam_RollNo'] != 'example_id':
                            student_id = row['Exam_RollNo']
                            student_roll_number = row['PU_Registration']
                            student_name = row['Name']
                            student_status = row['Status']

                            student_entry = df_summary[(df_summary['Exam_RollNo'] == student_id) &
                                                      (df_summary['PU_Registration'] == student_roll_number) &
                                                      (df_summary['Name'] == student_name)]

                            if student_entry.empty:
                                new_entry = {'Exam_RollNo': student_id, 'PU_Registration': student_roll_number,
                                             'Name': student_name}
                                new_entry[day_str] = student_status
                                df_summary = pd.concat([df_summary, pd.DataFrame([new_entry])], ignore_index=True)
                            else:
                                df_summary.loc[student_entry.index, day_str] = student_status

        for index, row in df_summary.iterrows():
            total_present = sum(1 for day in range(1, 32) if row.get(f"{day:02d}") == "Present")
            presence_percentage = (total_present / total_days) * 100 if total_days > 0 else 0
            df_summary.at[index, 'Presence Percentage'] = presence_percentage

        day_columns = [col for col in df_summary.columns if col.isdigit()]
        column_order = ['Exam_RollNo', 'PU_Registration', 'Name'] + ['Presence Percentage'] + day_columns
        df_summary = df_summary[column_order]

        try:
            df_summary.to_excel(summary_filename, index=False)
            messagebox.showinfo("Success", "Monthly summary generated successfully!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def face_recog(self):
        folder_path = "Attendance_sheet"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        metrics = {}

        def update_metrics(student_id, recognized_correctly):
            if student_id not in metrics:
                metrics[student_id] = {'TP': 0, 'FP': 0, 'FN': 0, 'total': 0}

            if recognized_correctly:
                metrics[student_id]['TP'] += 1
            else:
                metrics[student_id]['FP'] += 1
            metrics[student_id]['total'] += 1

            TP = metrics[student_id]['TP']
            FP = metrics[student_id]['FP']
            FN = metrics[student_id]['FN']
            total = metrics[student_id]['total']

            precision = TP / (TP + FP) if (TP + FP) > 0 else 0
            recall = TP / (TP + FN) if (TP + FN) > 0 else 0
            accuracy = TP / total if total > 0 else 0

            print(f"ID: {student_id} | Precision: {precision:.2f} | Recall: {recall:.2f} | Accuracy: {accuracy:.2f}")

        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(username='root', password='pass', host='localhost',
                                               database='face_recognition', port=3306)
                cursor = conn.cursor()

                cursor.execute("select Name from student where Exam_RollNo=" + str(id))
                n = cursor.fetchone()
                n = "+".join(n) if n else "Unknown"

                cursor.execute("select PU_Registration from student where Exam_RollNo=" + str(id))
                r = cursor.fetchone()
                r = "+".join(r) if r else "Unknown"

                cursor.execute("select Exam_RollNo from student where Exam_RollNo=" + str(id))
                i = cursor.fetchone()
                i = "+".join(map(str, i)) if i else "Unknown"

                attendance_marked = self.is_attendance_marked(i, n)

                if confidence > 85:
                    cv2.putText(img, f"Confidence:{confidence}%", (x, y - 105), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(img, f"Exam_RollNo:{i}", (x, y - 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    cv2.putText(img, f"Name:{n}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    cv2.putText(img, f"PU_Registration:{r}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)

                    if attendance_marked:
                        cv2.putText(img, "Already Marked", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0), 2)
                        update_metrics(i, True)
                    else:
                        self.mark_attend(i, r, n)
                        update_metrics(i, True)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 3)
                    # No confidence text for unknown
                    update_metrics("unknown", False)

                coord = [x, y, w, h]

            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer.create()
        clf.read("clf.xml")
        videoCap = cv2.VideoCapture(0)

        while True:
            ret, img = videoCap.read()
            img = recognize(img, clf, faceCascade)
            imgBackground = cv2.imread(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\background1.jpg")
            imgBackground = cv2.resize(imgBackground, (1366, 768))

            x_offset = (1366 - img.shape[1]) // 2
            y_offset = (768 - img.shape[0]) // 2

            imgBackground[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img

            cv2.imshow("Face Detector", imgBackground)
            if cv2.waitKey(1) == 13:  # Enter key to exit
                break

        videoCap.release()
        cv2.destroyAllWindows()

        self.generate_monthly_summary()


if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognition(root)
    root.mainloop()
