# backend/register.py

import cv2
import pickle
import numpy as np
import os

def collect_faces(name):
    facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(0)
    faces_data = []
    i = 0

    if not os.path.exists('data'):
        os.makedirs('data')

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop_img = frame[y:y+h, x:x+w, :]
            resized_img = cv2.resize(crop_img, (50, 50))

            if len(faces_data) < 100 and i % 10 == 0:
                faces_data.append(resized_img)
            i += 1

            cv2.putText(frame, str(len(faces_data)), (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

        cv2.imshow("Registering Face", frame)
        if cv2.waitKey(1) == 27 or len(faces_data) == 100:
            break

    video.release()
    cv2.destroyAllWindows()

    # Save face data
    faces_data = np.asarray(faces_data)
    faces_data = faces_data.reshape(len(faces_data), -1)

    names_path = 'data/names.pkl'
    faces_path = 'data/faces_data.pkl'

    if os.path.exists(names_path):
        with open(names_path, 'rb') as f:
            names = pickle.load(f)
        names.extend([name] * len(faces_data))
    else:
        names = [name] * len(faces_data)

    with open(names_path, 'wb') as f:
        pickle.dump(names, f)

    if os.path.exists(faces_path):
        with open(faces_path, 'rb') as f:
            faces = pickle.load(f)
        faces = np.append(faces, faces_data, axis=0)
    else:
        faces = faces_data

    with open(faces_path, 'wb') as f:
        pickle.dump(faces, f)

    return True
