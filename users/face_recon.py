import face_recognition
import cv2
import os

def face_video():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('img', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()


def face_login(loc):
    cam = cv2.VideoCapture(0)
    s, img = cam.read()
    if s:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        loc = (str(BASE_DIR) + loc)

        face_1_image = face_recognition.load_image_file(loc)
        face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        try:
            check = face_recognition.compare_faces(face_1_face_encoding, face_encodings)
        except:
            return False

        if check[0]:
            return True
        else:
            return False
