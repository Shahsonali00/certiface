import os
import tkinter as tk
from tkinter import RIDGE, Button, Frame, Label, Tk, Toplevel, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import pkg_resources
import pygame
from main import Face_Recognition_System
import mysql.connector

# Load the haarcascade file for face detection
haar = pkg_resources.resource_filename('cv2', 'data/haarcascade_frontalface_default.xml')


class Flogin:
    def __init__(self, root):
        self.root = root
        pygame.init()
        pygame.mixer.init()
        self.video_capture = cv2.VideoCapture(0)
        self.face_recog()

    def face_recog(self):
        self.video_capture = cv2.VideoCapture(0)

        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                user_name, predict = clf.predict(gray_image[y:y + h, x:x + w])

                confidence = int((100 * (1 - predict / 300)))

                # Connect to MySQL database
                conn = mysql.connector.connect(username='root', password='pass', host='localhost', database='face_recognition', port=3306)
                cursor = conn.cursor()

                cursor.execute("select fname from regteach where user_name=" + str(user_name))
                n = cursor.fetchone()

                # If no name is found for the user, set to "Unknown"
                if n is not None:
                    n = "+".join(n)
                else:
                    n = "Unknown"

                # Only proceed if the confidence is above a threshold and a valid user is found
                if confidence > 80 and n != "Unknown":
                    cv2.putText(img, f"user_name:{n}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64, 15, 223), 2)
                    self.login()  # Proceed with login
                    pygame.init()
                    pygame.mixer.init()
                    pygame.mixer.music.load("loginaudio.mp3")
                    pygame.mixer.music.play()
                    return True
                else:
                    # If face is not recognized or confidence is low
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 0), 3)

            return False

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face_LBPHFaceRecognizer.create()
        clf.read("clf_admin.xml")
        videoCap = cv2.VideoCapture(0)

        while True:
            ret, img = videoCap.read()
            if draw_boundray(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf):
                break
            imgBackground = cv2.imread(r"C:\Users\dell\Desktop\Python_Test_Project\Images_GUI\facelogin.jpg")
            imgBackground = cv2.resize(imgBackground, (1366, 768))
            x_offset = (1366 - img.shape[1]) // 2
            y_offset = (768 - img.shape[0]) // 2
            imgBackground[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img

            cv2.imshow("Face Detector", imgBackground)
            if cv2.waitKey(1) == 13:  # Enter key pressed
                break

        videoCap.release()
        cv2.destroyAllWindows()

    def login(self):
        # Proceed with the login if the face is recognized
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition_System(self.new_window)
        self.video_capture.release()  # Release webcam resource
        self.root.withdraw()  # Withdraw the main window

    def on_closing(self):
        self.video_capture.release()  # Release webcam resource
        self.root.destroy()  # Close the window


if __name__ == "__main__":
    root = tk.Tk()
    Flogin(root)
    root.mainloop()