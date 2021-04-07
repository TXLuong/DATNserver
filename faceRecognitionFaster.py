import face_recognition
import cv2
import numpy as np

# start web cam 
video_capture = cv2.VideoCapture(0)

# load anh de hoc cac feature cua anh 
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# load anh de hoc cac feature cua anh 
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# load anh de hoc cac feature cua anh 
luong_image = face_recognition.load_image_file("luong.jpg")
luong_face_encoding = face_recognition.face_encodings(luong_image)[0]


# array of known face 
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    luong_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "TXLuong"
]

# vi tri cua face 
face_locations = []
# face encoded
face_encodings = []
# ten face 
face_names = []

process_this_frame = True

while True:
    # Grab 1 frame cua webcam 
    ret, frame = video_capture.read()

    # resize 1/4 anh de khong can tinh toan nhieu 
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)\

    # Chuyen anh tu dang BGR cua Open CV -> RGB de phu hop vs model face_recognition su dung 
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # tim tat ca cac faces va face encodings 
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Hien thi 
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # scale tro ve kich thuoc ban dau
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # draw face area 
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # label name 
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # resulting image
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWinddows()

#https://github.com/ageitgey/face_recognition 
