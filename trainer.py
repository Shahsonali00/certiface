import cv2
import numpy as np
from PIL import Image
import os

# Path where you saved your dataset images
dataset_path = "data_img"  # Change to your folder name if different

# Create LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]
    face_samples = []
    ids = []
    for image_path in image_paths:
        # convert image to grayscale
        pil_img = Image.open(image_path).convert('L')
        img_numpy = np.array(pil_img, 'uint8')
        # get id from image filename (assuming filename format: User.id.number.jpg)
        id = int(os.path.split(image_path)[-1].split('.')[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)
    return face_samples, ids

print("\n[INFO] Training faces. Please wait ...")
faces, ids = get_images_and_labels(dataset_path)
recognizer.train(faces, np.array(ids))

# Save the trained model
recognizer.save("clf.xml")
print("\n[INFO] Training complete. Model saved as clf.xml")
