import face_recognition
import cv2  
import os
import pickle
import time
import numpy as np
#import db
# myDB = db.connectDb()
# cursor = myDB.cursor()

print(cv2.version)

fpsReport=0
scaleFactor=.25

Encodings = []
Names = []

with open('train.pkl', 'rb') as f:
    Names = pickle.load(f)
    Encodings = pickle.load(f)
font = cv2.FONT_HERSHEY_SIMPLEX

cam = cv2.VideoCapture(0)

timeStamp = time.time()
while True:
    _,frame=cam.read()
    frameSmall=cv2.resize(frame,(0,0),fx=scaleFactor,fy=scaleFactor)
    # frameRGB=cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)
    frameRGB = frameSmall[:, :, ::-1]
    facePositions=face_recognition.face_locations(frameRGB,model='cnn')
    allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
    for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
        name='Unkown Person'
        matches=face_recognition.compare_faces(Encodings,face_encoding)
        # if True in matches:
        #     first_match_index=matches.index(True)
        #     name=Names[first_match_index]
        face_distances = face_recognition.face_distance(Encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = Names[best_match_index]
        top=int(top/scaleFactor)
        right=int(right/scaleFactor)
        bottom=int(bottom/scaleFactor)
        left=int(left/scaleFactor)
        
        cv2.rectangle(frame,(left,top),(right, bottom),(0,0,255),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,0,255),2)
        print("Day la mat cua: ", name)
        data = ("in", name)
        # db.updateStudentsStatus(myDB, cursor, data)

    dt = time.time()-timeStamp
    fps = 1/dt
    fpsReport = .90*fpsReport + .1*fps
    print('fps is:', round(fpsReport, 1))
    timeStamp = time.time()
    cv2.rectangle(frame, (0, 0), (100, 40), (0, 0, 255), -1)
    cv2.putText(frame, str(round(fpsReport, 1)) + 'fps',
                (0, 25), font, .75, (0, 255, 255, 2))
    cv2.imshow('Picture', frame)
    cv2.moveWindow('Picture', 0, 0)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
