import face_recognition
import cv2
import os

WORKING_DIR = os.getcwd()
KNOWN_FACES_DIR = os.path.join(WORKING_DIR, "known_faces")

NAMES = os.listdir(KNOWN_FACES_DIR)
images = os.listdir(os.path.join(KNOWN_FACES_DIR, NAMES[0]))
image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, NAMES[0], images[0]))
        
encoding = face_recognition.face_encodings(image)[0]

