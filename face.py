!/usr/bin/python

import sys

import dlib

import cv2

detector = dlib.get_frontal_face_detector()
win = dlib.image_window()
# Open the device at the ID 0

cap = cv2.VideoCapture(0)

#Check whether user selected camera is opened successfully.

if not (cap.isOpened()):

    print("Could not open video device")

while(True):

    # Capture frame-by-frame
    
    ret, frame = cap.read()
    img = im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Display the resulting frame
    
    cv2.imshow("preview",frame)
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            i, d.left(), d.top(), d.right(), d.bottom()))
    
    win.clear_overlay()
    win.set_image(img)
    win.add_overlay(dets)
    dlib.hit_enter_to_continue()
    
    #Waits for a user input to quit the application
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
    
        break
    
    # When everything done, release the capture

cap.release()

cv2.destroyAllWindows()

# Finally, if you really want to you can ask the detector to tell you the score
# for each detection.  The score is bigger for more confident detections.
# The third argument to run is an optional adjustment to the detection threshold,
# where a negative value will return more detections and a positive value fewer.
# Also, the idx tells you which of the face sub-detectors matched.  This can be
# used to broadly identify faces in different orientations.
if (len(sys.argv[1:]) > 0):
    img = dlib.load_rgb_image(sys.argv[1])
    dets, scores, idx = detector.run(img, 1, -1)
    for i, d in enumerate(dets):
        print("Detection {}, score: {}, face_type:{}".format(
            d, scores[i], idx[i]))