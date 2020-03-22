#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import face_recognition
import os
import numpy as np
from file_name import get_encoding_file_name
import cv2
import time
import matplotlib.pyplot as plt
import random
from datetime import datetime

WORKING_DIR = os.getcwd()
KNOWN_FACES_DIR = os.path.join(WORKING_DIR, "known_faces")
ENTRANCE_LOG_DIR = os.path.join(WORKING_DIR, "entrances")

NAMES = os.listdir(KNOWN_FACES_DIR)
MODEL = "hog"
TOLERANCE = 0.5

def load_encodings(name):
    NAME_DIR = os.path.join(KNOWN_FACES_DIR, name)
    if not os.path.isdir(NAME_DIR):
        print("{name} is invalid. Are you sure there is such a directory under known_faces?")
        return
    
    encoding_file_name = get_encoding_file_name(name)
    encoding_file_path = os.path.join(NAME_DIR, encoding_file_name)
    if not os.path.isfile(encoding_file_path):
        print("{name} is not encoded. Run encode_names.py before identifying faces.")

    return np.load(encoding_file_path, allow_pickle = True)

def load_all_people():
    people = []
    for name in NAMES:
        people.append({"name": name})
        people[-1]["encodings"] = load_encodings(name)
    
    return people

def check_match(encoding, person):
    return face_recognition.compare_faces(person["encodings"], encoding, TOLERANCE)
    
def find_identity(encoding, people):
    for person in people:
        if True in check_match(encoding, person):
            return person["name"]
    else:
        return "Unknown person"

def get_identity(image, known_people):
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    names = []
    for face_encoding, face_location in zip(encodings, locations):
        name = find_identity(face_encoding, known_people)
        names.append(name)
    
    return names

def get_landmarks(image):
    return face_recognition.face_landmarks(image)
    

def draw_landmarks(image, faces):
    for face in faces:
        for key in face.keys():
            vectors = face[key]
            for i,vector in enumerate(vectors[1:]):
                cv2.line(image, vectors[i], vector, (255,0,0), 1)
                
def get_area_of_eyes(landmarks):
    areas = []
    for face in landmarks:
        chin_area = (face['chin'][0][0] - face['chin'][-1][0])**2 + (face['chin'][0][1] - face['chin'][-1][1])**2
        left_eye = face['left_eye']
        right_eye = face['right_eye']
        areas.append(get_area(left_eye)/chin_area + get_area(right_eye)/chin_area)
    
    return areas
        
def get_area(shape):
    shape_array = np.array(shape)
    center = np.sum(shape_array, axis = 0)/shape_array.shape[0]
    area = 0
    for i, corner in enumerate(shape_array):
        triangle = np.array([corner, shape[(i+1)%shape_array.shape[0]], center])
        area += get_triangle_area(triangle)
    return area

def get_triangle_area(coordinates):
    if coordinates.shape[0] != 3:
        return -1e5
    area = 0
    for i, coordinate in enumerate(coordinates):
        area += coordinate[0]*(coordinates[(i+1)%3][1]-coordinates[(i+2)%3][1])/2
    return area

def get_face_direction(landmarks):
    directions = []
    for face in landmarks:
        nose_bridge = np.array(face['nose_bridge'])
        chin_length = ((face['chin'][0][0] - face['chin'][-1][0])**2 + (face['chin'][0][1] - face['chin'][-1][1])**2)**0.5
        direction = (nose_bridge[0][0] - nose_bridge[-1][0])/chin_length
        directions.append(direction)
    return directions

# def make_random_tests():
#     random_tests = []
    
# def eye_test(standard_eye_areas, name, people):
#     total_standard_area = np.sum(standard_eye_areas)
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 135)
#     print("Stay normal...")
#     successive_frames = 0
#     for _ in range(150):
#         ret, image = cap.read()
#         landmarks = get_landmarks(image)
#         if not landmarks:
#             print("Identification failed.")
#             return False
#         if np.sum(np.array(get_area_of_eyes(landmarks))) < 1.5*total_standard_area:
#             successive_frames += 1
#             if successive_frames > 10:
#                 break
#         else:
#             successive_frames = 0
#     else:
#         print("Identification failed.")
#         return False
    
#     print("Open your eyes widely...")
#     successive_frames = 0
#     for _ in range(150):
#         ret, image = cap.read()
#         landmarks = get_landmarks(image)
#         if not landmarks:
#             print("Identification failed.")
#             return False
#         if np.sum(np.array(get_area_of_eyes(landmarks))) > 1.5*total_standard_area:
#             successive_frames += 1
#             if successive_frames > 10:
#                 if get_identity(image, people)[0] == name:
#                     print("Identification successful.")
#                     return True
#         else:
#             successive_frames = 0
        
#     else:
#         print("Identification failed.")
#         return False

def get_wideness_of_mouth(landmarks):
    widenesses = []
    for face in landmarks:
        top_lip = face['top_lip']
        bottom_lip = face['bottom_lip']
        
        top_point = np.min(np.array(top_lip)[:,1:])
        bottom_point = np.max(np.array(bottom_lip)[:,1:])
        left_point = np.min(np.array(bottom_lip)[:,:1])
        right_point = np.max(np.array(bottom_lip)[:,:1])
        widenesses.append((bottom_point-top_point)/(right_point-left_point))

    return widenesses


# def mouth_test(standard_mouth_wideness, name, people):
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 135)
#     print("Stay normal...")
#     successive_frames = 0
#     for _ in range(150):
#         ret, image = cap.read()
#         landmarks = get_landmarks(image)
#         if not landmarks:
#             print("Identification failed.")
#             return False
#         if np.sum(np.array(get_wideness_of_mouth(landmarks))) < 1.5*standard_mouth_wideness:
#             successive_frames += 1
#             if successive_frames > 10:
#                 break
#         else:
#             successive_frames = 0
#     else:
#         print("Identification failed.")
#         return False
    
#     print("Open your mouth widely...")
#     successive_frames = 0
#     for _ in range(150):
#         ret, image = cap.read()
#         landmarks = get_landmarks(image)
#         if not landmarks:
#             print("Identification failed.")
#             return False
#         if np.array(get_wideness_of_mouth(landmarks)) > 1.5*standard_mouth_wideness:
#             successive_frames += 1
#             if successive_frames > 10:
#                 if get_identity(image, people)[0] == name:
#                     print("Identification successful.")
#                     return True
#         else:
#             successive_frames = 0
        
#     else:
#         print("Identification failed.")
#         return False

def default_condition(evaluated_value, threshold):
    return evaluated_value > threshold

def reverse_condition(evaluated_value, threshold):
    return evaluated_value < threshold

def test(threshold, evaluation_function, message, condition = default_condition):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 135)
    print("Stay normal...")
    successive_frames = 0
    for _ in range(200):
        ret, image = cap.read()
        landmarks = get_landmarks(image)
        if not landmarks:
            # print("Identification failed.")
            return [False, []]
        if not condition(evaluation_function(landmarks)[0], threshold):
            successive_frames += 1
            if successive_frames > 10:
                break
        else:
            successive_frames = 0
    else:
        # print("Identification failed.")
        return [False, []]
    
    print(message)
    successive_frames = 0
    for _ in range(200):
        ret, image = cap.read()
        landmarks = get_landmarks(image)
        if not landmarks:
            # print("Identification failed.")
            return [False, []]
        if condition(evaluation_function(landmarks)[0], threshold):
            successive_frames += 1
            if successive_frames > 10:
                if get_identity(image, people)[0] == name:
                    # print("Identification successful.")
                    return [True, image]
        else:
            successive_frames = 0
        
    else:
        # print("Identification failed.")
        return [False, []]
    
NUMBER_OF_TESTS = 1

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    people = load_all_people()
    ret, image = cap.read()
    cap.release()
    names = get_identity(image, people)
    if len(names) == 0:
        print("No known faces found.")
    else:
        name = names[0]
        print(f"Hi {name}!")
        standard_image_path = os.path.join(KNOWN_FACES_DIR, name, "standard.jpg")
        if not os.path.exists(standard_image_path):
            print("No standard faces found.")
        else:
            standard_image = cv2.imread(standard_image_path)
            standard_landmarks = get_landmarks(standard_image)
            standard_eye_areas = get_area_of_eyes(standard_landmarks)[0]
            standard_mouth_wideness = get_wideness_of_mouth(standard_landmarks)[0]
            direction_threshold = 0.02
            
            for _ in range(NUMBER_OF_TESTS):
                test_result = eval(random.choice(['test(1.5*standard_mouth_wideness, get_wideness_of_mouth, "Open your mouth...")',\
                                    'test(1.4*standard_eye_areas, get_area_of_eyes, "Open your eyes...")',\
                                    'test(-direction_threshold, get_face_direction, "Turn your head to left...", reverse_condition)',\
                                    'test(direction_threshold, get_face_direction, "Turn your head to right...")']))
            
                if not (test_result[0] and (get_identity(test_result[1], people)[0] == name)):
                    print("You are not allowed to enter.")
                    break
            
            else:
                now = datetime.now()
                image_name = f"{now.strftime('%d%m%Y_%H_%M_%S')}.jpg"
                image_path = os.path.join(ENTRANCE_LOG_DIR, name)
                if not os.path.exists(image_path):
                    os.mkdir(image_path)
                cv2.imwrite(os.path.join(image_path, image_name), test_result[1])
                print("You are allowed to enter.")
            
            

# if __name__ == "__main__":
#     show_landmarks= True
#     cap = cv2.VideoCapture(0)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 135)
#     people = load_all_people()
#     eye_areas = np.zeros((10, 2))
#     fps = 20
#     while(True):
#         start = time.time()
#         ret, image = cap.read()
#         landmarks = get_landmarks(image)
#         print(get_face_direction(landmarks))
#         # print(np.sum(eye_areas[0]))
#         if show_landmarks:
#             empty_image = np.ones(image.shape)*255
#             draw_landmarks(empty_image, landmarks)
#         cv2.imshow("deneme", empty_image)
#         if cv2.waitKey(1) == ord("q"):
#             break
#         fps = 1/(time.time()-start)
#         print(f"fps = {fps}")
        
#     cv2.destroyAllWindows()
#     cap.release()
