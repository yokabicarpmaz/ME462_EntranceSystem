#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import face_recognition
import os
import numpy as np
from file_name import get_encoding_file_name

WORKING_DIR = os.getcwd()
KNOWN_FACES_DIR = os.path.join(WORKING_DIR, "known_faces")

NAMES = os.listdir(KNOWN_FACES_DIR)

def encode_name(name):
    NAME_DIR = os.path.join(KNOWN_FACES_DIR, name)
    if not os.path.isdir(NAME_DIR):
        print("{name} is invalid as a name. Are you sure there is such a directory under known_faces?")
        return 
    
    print(f"Encodings for {name} are being calculated...")
    file_names = os.listdir(NAME_DIR)
    # if get_encoding_file_name(name) in file_names:
    #     print("Encodings for {name} already exist.")
    image_names = [file_name for file_name in file_names if (file_name.split(".")[1] == "jpg"\
                                                                or file_name.split(".")[1] == "jpeg"\
                                                                    or file_name.split(".")[1] == "png")]
    encodings = []
    for image_name in image_names:
        image = face_recognition.load_image_file(os.path.join(NAME_DIR, image_name))
        all_face_encodings = face_recognition.face_encodings(image)
        if all_face_encodings:
            encoding = all_face_encodings[0]
            encodings.append(encoding)
        
    print(f"{len(encodings)} faces are encoded for {name}")
    encoding_file_name = get_encoding_file_name(name)
    np.save(os.path.join(NAME_DIR, encoding_file_name), encodings)
    print(f"Encodings for {name} are saved.")
   

def encode_names():
    for name in NAMES:
        encode_name(name)


if __name__ == "__main__":
    encode_names()




