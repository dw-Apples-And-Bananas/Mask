import mediapipe as mp
import cv2
import numpy as np
from face import *


def idx(connections):
    s = set()
    for c in list(connections):
        s.add(c[0])
        s.add(c[1])
    return list(s)


mp_face_mesh = mp.solutions.face_mesh

face_tesselation = idx(mp_face_mesh.FACEMESH_TESSELATION)


cap = cv2.VideoCapture(0)
_, img = cap.read()
vid = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 16, (img.shape[1],img.shape[0]))

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.25,
        min_tracking_confidence=0.25) as face_mesh:
    while cap.isOpened():
        _, image = cap.read()
        if not _:
            print("Empty Camera")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        cv2.circle(image, (500,500), 1000, (255,255,255), -1)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                lms = face_landmarks.landmark
                tesselation = {}

                for index in face_tesselation:
                    x = int(lms[index].x * image.shape[1])
                    y = int(lms[index].y * image.shape[0])
                    tesselation[index] = (x,y)
                    if False:
                        cv2.circle(image, (x,y), 3, (0,0,255), -1)
                        cv2.putText(image, str(index), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1)

                oval = Oval(lms, image)
                tesselation = Tesselation(lms, image)
                left_eye = LeftEye(lms, image)
                right_eye = RightEye(lms, image)

                nose = Nose(lms, image)
                cv2.polylines(image, [nose.np_points], False, (0,100,50), 2)

                cv2.polylines(image, [oval.np_points], True, (0,0,0), 1)

                cv2.circle(image, (left_eye.center.x, left_eye.center.y), 3, (0,0,0), -1)
                cv2.circle(image, (right_eye.center.x, right_eye.center.y), 3, (0,0,0), -1)

                #cv2.polylines(image, [np.array([[p.x,p.y] for p in left_eye.points], np.int32)], True, (0,0,0), 2)
                #cv2.polylines(image, [np.array([[p.x,p.y] for p in right_eye.points], np.int32)], True, (0,0,0), 2)
                #cv2.fillPoly(image, [np.array(outline_pos, np.int32)], (0,0,0))

        #vid.write(image)
        #cv2.imshow("webcam", cv2.flip(image, 1))
        cv2.imshow("webcam", image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
