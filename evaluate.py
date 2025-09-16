import cv2
import os
from sklearn.metrics import accuracy_score, f1_score
from PIL import Image
import numpy as np

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load trained face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("clf.xml")  # This must match the file trained in train.py

# Match these labels to IDs used in image filenames: User.ID.ImageNo.jpg
label_dict = {
    1: "Alice",
    2: "Bob",
    3: "Charlie"
    # Add more as needed
}

# Folder structure: test_faces/Name/*.jpg
test_folder = "test_faces"
y_true = []
y_pred = []

for person_name in os.listdir(test_folder):
    person_path = os.path.join(test_folder, person_name)
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(roi)
            predicted_name = label_dict.get(label, "Unknown")

            y_true.append(person_name)
            y_pred.append(predicted_name)

# Calculate and print accuracy and F1 score
accuracy = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred, average='macro')

print("Accuracy:", accuracy)
print("F1 Score:", f1)
