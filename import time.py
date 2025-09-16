import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, Button, messagebox, simpledialog
from PIL import Image, ImageTk

class FaceRecognitionLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Login")
        self.root.geometry("800x600")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.user_data = {}  # Dictionary to store user data (id -> name)

        # GUI components
        self.label = Label(self.root)
        self.label.place(x=0, y=0, width=800, height=600)

        self.register_button = Button(self.root, text="Register", command=self.register_user)
        self.register_button.place(x=200, y=550, width=100, height=40)

        self.login_button = Button(self.root, text="Login", command=self.login_user)
        self.login_button.place(x=500, y=550, width=100, height=40)

        self.capture = cv2.VideoCapture(0)

        # Train the recognizer when the application starts
        self.train_recognizer()

        self.capture_face()

    def capture_face(self):
        ret, frame = self.capture.read()
        frame = cv2.flip(frame, 1)  # Mirror the frame horizontally for better user experience

        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]

            # Ensure that the recognizer is trained before prediction
            if self.recognizer and len(self.user_data) > 0:
                face_id, confidence = self.recognizer.predict(face_roi)

                if confidence < 50:  # Adjust confidence threshold as needed
                    user_name = self.user_data.get(face_id, "Unknown")
                    cv2.putText(frame, f"Welcome, {user_name}!", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Face not recognized", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Convert OpenCV frame to a format compatible with tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = ImageTk.PhotoImage(image=img)

        # Update the label with the new image
        self.label.config(image=img)
        self.label.image = img  # Keep a reference to prevent the image from being garbage collected

        self.root.after(100, self.capture_face)

    def register_user(self):
        user_name = simpledialog.askstring("Register", "Enter your name:")
        if user_name:
            user_id = len(self.user_data) + 1
            self.user_data[user_id] = user_name

            # Save user's face for training
            face_id = str(user_id)
            folder_path = f"dataset/{user_id}"

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            count = 0
            while count < 30:
                ret, frame = self.capture.read()
                frame = cv2.flip(frame, 1)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    face_roi = gray[y:y + h, x:x + w]
                    cv2.imwrite(f"{folder_path}/{face_id}_{count}.jpg", face_roi)
                    count += 1

                cv2.imshow('Capturing', frame)
                cv2.waitKey(100)

            messagebox.showinfo("Registration", f"Registration successful for {user_name}")

            # Train the recognizer after registration
            self.train_recognizer()

    def train_recognizer(self):
        faces = []
        labels = []

        for user_id, user_name in self.user_data.items():
            folder_path = f"dataset/{user_id}"
            for filename in os.listdir(folder_path):
                if filename.endswith(".jpg"):
                    img_path = os.path.join(folder_path, filename)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    faces.append(img)
                    labels.append(user_id)

        if faces and labels:
            self.recognizer.train(faces, np.array(labels))

    def login_user(self):
        if not self.user_data:
            messagebox.showwarning("Login", "No registered users. Please register first.")
            return

        ret, frame = self.capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]

            # Ensure that the recognizer is trained before prediction
            if self.recognizer and len(self.user_data) > 0:
                face_id, confidence = self.recognizer.predict(face_roi)

                if confidence < 50:  # Adjust confidence threshold as needed
                    user_name = self.user_data.get(face_id, "Unknown")
                    messagebox.showinfo("Login", f"Welcome, {user_name}!")
                else:
                    messagebox.showwarning("Login", "Face not recognized!")

    def on_closing(self):
        self.capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionLogin(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()