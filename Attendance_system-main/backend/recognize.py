from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def recognize_faces():
    names_path = 'data/names.pkl'
    faces_path = 'data/faces_data.pkl'

    if not os.path.exists(names_path) or not os.path.exists(faces_path):
        return {"error": "Face data not found"}

    with open(names_path, 'rb') as f:
        LABELS = pickle.load(f)
    with open(faces_path, 'rb') as f:
        FACES = pickle.load(f)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, LABELS)

    facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video = cv2.VideoCapture(0)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/Attendance_{today}.csv"

    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["NAME", "TIME"])

    marked = set()
    recognized_people = []

    start_time = time.time()  # Track when we started
    timeout = 10              # Stop after 10 seconds

    while True:
        elapsed = time.time() - start_time
        if elapsed >= timeout:
            break

        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            crop = frame[y:y+h, x:x+w, :]
            resized = cv2.resize(crop, (50, 50)).flatten().reshape(1, -1)
            prediction = knn.predict(resized)
            name = prediction[0]

            cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 255), 2)

            if name not in marked:
                marked.add(name)
                recognized_people.append(name)
                time_now = datetime.now().strftime("%H:%M:%S")

                with open(filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([name, time_now])
                speak(f"{name}, your attendance is marked.")

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) == 27:
            break

    video.release()
    cv2.destroyAllWindows()

    return {"recognized": list(set(recognized_people))}
